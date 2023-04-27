import os
import json
import boto3
import botocore
import psycopg2
import tempfile
from urllib.parse import urlparse
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class AWSClient():
    def __init__(self, config):
        # validations
        if "profile_name" in config and ("access_key_id" in config or "secret_access_key" in config):
            raise Exception("Only one of ('profile_name') or ('access_key_id' and 'secret_access_key') must be set!")

        if not "profile_name" in config and not "access_key_id" in config and not "secret_access_key" in config:
            config["profile_name"] = "default"
        
        if not "pdf_bucket" in config:
            raise Exception("Config 'pdf_bucket' is required!")
        
        if not "cache_bucket" in config:
            raise Exception("Config 'cache_bucket' is required!")
        
        self.pdf_bucket_name = config["pdf_bucket"]
        self.cache_bucket_name = config["cache_bucket"]

        # initialize client
        if "profile_name" in config:
            self.session = boto3.Session(profile_name=config["profile_name"])
        else:
            self.session = boto3.Session(
                aws_access_key_id=config["access_key_id"],
                aws_secret_access_key=config["secret_access_key"],
            )

        # define resources
        self.tmp_dir = tempfile.gettempdir()
        self.s3_resource = self.session.resource("s3")
        self.pdf_bucket = self.s3_resource.Bucket(self.pdf_bucket_name)
        self.cache_bucket = self.s3_resource.Bucket(self.cache_bucket_name)

        if "pg_db" not in config:
            config["pg_db"] = "bluewave"
            self.db_name = config["pg_db"]
        if "pg_table" not in config:
            config["pg_table"] = "results"
            self.table_name = config["pg_table"]

        print("Trying to connect to DB...")

        self.pg_engine = psycopg2.connect(
            user=config["pg_username"],
            password=config["pg_password"],
            host=config["pg_host"],
            port=config["pg_port"],
        )
        self.pg_engine.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.pg_engine.cursor()
        self.create_db_if_not_exists()
        self.cleanup_pg_connection()

        self.pg_engine = psycopg2.connect(
            user=config["pg_username"],
            password=config["pg_password"],
            host=config["pg_host"],
            port=config["pg_port"],
            database=config["pg_db"]
        )
        self.cursor = self.pg_engine.cursor()
        self.create_table_if_not_exists()
        print("Successfully connected to DB!")
    
    def extract_filename_from_s3_url(self, s3_url):
        parser = urlparse(s3_url, allow_fragments=False)
        return parser.path.lstrip("/")

    def download_pdf_from_s3(self, file_name):
        file_name = self.extract_filename_from_s3_url(file_name)
        print(f"Downloading pdf file: {file_name}")
        tmp_file_path = os.path.join(self.tmp_dir, file_name)
        self.pdf_bucket.download_file(file_name, tmp_file_path)
        return tmp_file_path
    
    def download_cache_from_s3(self, file_name):
        file_name = os.path.basename(file_name)
        try:
            self.s3_resource.Object(self.cache_bucket_name, file_name).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("Cache not found")
                return None
            else:
                print(f"Error occurred while trying to read cache: {e.response['Error']['Code']}")
                return None
        else:
            print("Cache found!")
            self.cache_bucket.download_file(file_name, file_name)
            return file_name
    
    def upload_cache_to_s3(self, cache_json, file_path):
        s3_object = self.s3_resource.Object(self.cache_bucket_name, os.path.basename(file_path))
        s3_object.put(
            Body=(bytes(json.dumps(cache_json).encode("UTF-8")))
        )
    
    def create_db_if_not_exists(self):
        self.cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}'")
        exists = self.cursor.fetchone()
        if not exists:
            self.cursor.execute(f"CREATE DATABASE {self.db_name}")

    def create_table_if_not_exists(self):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id serial PRIMARY KEY,
            comparison_data jsonb NOT NULL,
            comparison_date timestamp not null default CURRENT_TIMESTAMP
            )"""
        )
    
    def cleanup_pg_connection(self):
        self.pg_engine.commit()
        self.cursor.close()
        self.pg_engine.close()
    
    def insert_result_into_rds_pg_table(self, result):
        insert_query = f"INSERT INTO {self.table_name} (comparison_data) VALUES (%s)"
        self.cursor.execute(insert_query, (json.dumps(result),))
        self.cleanup_pg_connection()
