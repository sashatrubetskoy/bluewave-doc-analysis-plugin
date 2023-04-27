# Bluewave

This is a Python script to analyze the similarity of two PDFs.

### Usage
To run this, an example would be:

```
from bluewave.compare_pdfs import compare_pdf_files

filenames = ["file1.pdf", "file2.pdf"]
result = compare_pdf_files(filenames,
                           methods=False,
                           pretty_print=False,
                           verbose=True,
                           regen_cache=True,
                           sidecar_only=False,
                           no_importance=False)
```

To run with AWS connection

```
filenames = ["sample_files/sample_file_1.pdf", "sample_files/sample_file_2.pdf"]
aws_config = {
    "profile_name": "default",
    "pdf_bucket": "bluewave2023",
    "cache_bucket": "bluewave2023-cache",
    "pg_username": "postgres",
    "pg_password": "gizmo1228",
    "pg_host": "bluewave.chwv9x0hbowb.us-east-2.rds.amazonaws.com",
    "pg_port": 5432,
    "pg_db": "bluewave",
    "pg_table": "results"
}

result = compare_pdf_files(filenames,
                           methods=False,
                           pretty_print=False,
                           verbose=True,
                           regen_cache=True,
                           sidecar_only=False,
                           no_importance=False,
                           aws_config=aws_config)
```
