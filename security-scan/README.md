# Scan an AWS account for security holes

Scan, and report or optionally repair security holes in an AWS cloud environment

## S3 Bucket Scan

Check that S3 buckets are encrypted, as are their contents, and that connections to them require TLS. Optionally, repair any of these issues if they exist. This can be run from the Makefile with the following commands:

* **make list-buckets**:
	`./scanBuckets.py list`
This lists all of the buckets we have in our account.

* **make scan-buckets**:
	./scanBuckets.py scan
* **bucket-logging**:
	./scanBuckets.py logging
* **fix-buckets**:
	./scanBuckets.py modify
* **bucket-encryption**:
	./scanBuckets.py encryption

