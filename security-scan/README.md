# Scan an AWS account for security holes

Scan, and report or optionally repair security holes in an AWS cloud environment

## S3 Bucket Scan

Check that S3 buckets are encrypted, as are their contents, and that connections to them require TLS. Optionally, repair any of these issues if they exist. This can be run from the Makefile with the following commands:

* **make list-buckets**: This invokes the command:

	`./scanBuckets.py list` which lists all of the buckets we have in our account.

* **make scan-buckets**: This invokes the command:

	`./scanBuckets.py scan` which examines all buckets for security issues and generates a report on the command line.

* **bucket-logging**: This invokes the command:

	`./scanBuckets.py logging` which indicates whether a bucket has logging turned on or not.

* **fix-buckets**: This invokes the command:

	`./scanBuckets.py modify` which looks for security issues and, if found, attempts to repair them in place, and then re-install them.

* **bucket-encryption**: This invokes the command:

	`./scanBuckets.py encryption` which describes a bucket's encryption status.



