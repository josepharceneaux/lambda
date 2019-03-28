#! /usr/bin/env python3


import os
import sys
import shutil
import subprocess
import re
import zipfile
import datetime
import requests
import boto3
import argparse


LAMBDA_CLIENT = boto3.client('lambda')
LATEST_DEPLOYMENT_FILE_PATH = 'deployments/latest_deployment.zip'


def get_immediate_subdirectories(parent_directory):
    """
    :param str parent_directory: The directory we want to get the subdirectories of.
    :return list:
    """
    return [name for name in os.listdir(parent_directory)
            if os.path.isdir(os.path.join(parent_directory, name))]


def get_latest_deployment_directory(deployment_parent_directory='./deployments'):
    """
    Return the latest deployment directory we've built
    """

    # Get all the deployment versions
    all_deployment_directories = get_immediate_subdirectories(deployment_parent_directory)
    all_deployment_directories.sort()
    if len(all_deployment_directories) >= 1:
        latest = all_deployment_directories[-1]
        pattern = 'deployment_[0-9]*'
        if re.search(pattern, latest):
            return latest

    return None
    

# If we don't want to garbage collect, set this to None
MAX_VERSIONS = 10


def make_deployment_dir(deployment_parent_directory='deployments'):
    """
    Creates a versioned deployment directory under a root deployment directory.

    :param deployment_parent_directory: The name of the new directory where deployments will go.
    :return tuple (str, str):
    """

    # race condition. (http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary).
    if not deployment_parent_directory or not os.path.isdir(deployment_parent_directory):
        os.mkdir(deployment_parent_directory)
        deployment_name = 'deployment_0'
        new_deployment_dir_path = "{}/{}".format(deployment_parent_directory, deployment_name)
        os.mkdir(new_deployment_dir_path)
        return new_deployment_dir_path

    # Get the last deployment
    last_deployment_directory = get_latest_deployment_directory(deployment_parent_directory)
    if not last_deployment_directory:
        deployment_name = 'deployment_0'
        new_deployment_dir_path = "{0}/{1}".format(deployment_parent_directory, deployment_name)
        if not os.path.exists(new_deployment_dir_path):
            os.mkdir(new_deployment_dir_path)
        return new_deployment_dir_path

    last_version_number = int(last_deployment_directory.split("_")[1])
    this_version_number = last_version_number + 1
    # We only keep MAX_VERSIONS deployments, unless that's None
    if MAX_VERSIONS and last_version_number >= MAX_VERSIONS:
        this_version_number = MAX_VERSIONS

    deployment_name = "deployment_{0}".format(this_version_number)
    new_deployment_dir_path = "{0}/{1}".format(deployment_parent_directory, deployment_name)
    if not os.path.exists(new_deployment_dir_path):
        os.mkdir(new_deployment_dir_path)

    return new_deployment_dir_path


def copy_virtual_env_libs(deployment_dir, lib64=False):
    """
    Copies the installed libraries from the virtual environment library dirs.

    :param deployment_dir: The name of the new deployment directory before zipping.
    :param lib64: Boolean value if python lib64 packages are to be copied.
    """

    if 'real_prefix' in dir(sys):
        # If we're in a virtual environment, this will have a value
        venv_root_dir = sys.real_prefix
    else:
        # Otherwise use the system environment
        venv_root_dir = sys.prefix

    package_dir = "{}/lib/python3.7/site-packages/".format(venv_root_dir)
    package64_dir = "{}/lib64/python2.7/site-packages/".format(venv_root_dir)
    print("Copying packages from environment {} to {}".format(package_dir, deployment_dir))

    if os.path.exists(package_dir):
        cmd = "cp -r {0}* {1}".format(package_dir, deployment_dir)
        subprocess.call(cmd, shell=True)
        if os.path.exists(package64_dir):
            cmd = "cp -r {0}* {1}".format(package64_dir, deployment_dir)
            subprocess.call(cmd, shell=True)
    else:
        raise UserWarning('Virtual environment folder {} not found.'.format(package_dir))


def zipdir(dir_path=None, zip_file_path=None, include_dir_in_zip=False):
    """
    Create a zip archive from a directory.
    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations.

    :param str dir_path: path to the directory to archive. This is the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.
    :param str zip_file_path: path to the output zip file. This can be an absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")
    :param bool include_dir_in_zip: indicator whether the top level directory should
    be included in the archive or omitted. (default False)
    """

    if not os.path.isdir(dir_path):
        raise OSError("Directory path argument {} is not a directory".format(dir_path))

    if not zip_file_path:
        zip_file_path = dir_path + ".zip"
    parent_dir, dir_to_zip = os.path.split(dir_path)

    # Function to prepare the proper archive path
    def trim_path(path):
        archive_path = path.replace(parent_dir, "", 1)
        if parent_dir:
            archive_path = archive_path.replace(os.path.sep, "", 1)
        if not include_dir_in_zip:
            archive_path = archive_path.replace(dir_to_zip + os.path.sep, "", 1)
        return os.path.normcase(archive_path)

    out_file = zipfile.ZipFile(zip_file_path, "w", compression=zipfile.ZIP_DEFLATED)
    for (archive_dir_path, dir_names, file_names) in os.walk(dir_path):
        for file_name in file_names:
            file_path = os.path.join(archive_dir_path, file_name)
            out_file.write(file_path, trim_path(file_path))

        # Make sure we get empty directories as well
        if not file_names and not dir_names:
            zip_info = zipfile.ZipInfo(trim_path(archive_dir_path) + "/")
            out_file.writestr(zip_info, "")
    out_file.close()


FILE_LIST_FILE = "files.txt"


def copy_deployment_files(deployment_dir):
    """
    Puts deployment files in a specified deployment directory.
    :param str deployment_dir:
    """
    if os.path.isfile(FILE_LIST_FILE):
        file_list = [line.rstrip('\n') for line in open(FILE_LIST_FILE)]
    else:
        print("No files .txt")


def build_lambda_zipfile():
    deployment_dir = make_deployment_dir()
    print("Building Lambda zip file from {}".format(deployment_dir))
    copy_deployment_files(deployment_dir)
    copy_virtual_env_libs(deployment_dir, lib64=False)
    new_zipfile = "deployments/{}.zip".format(deployment_dir.split('/')[-1])
    zipdir(dir_path='deployments', zip_file_path=new_zipfile)
    print("New zip will be {}".format(new_zipfile))


def install_lambda_zipfile():
    print("Deploying Lambda")
    deployment_dir = make_deployment_dir()
    # copy_virtual_env_libs("foo")


parser = argparse.ArgumentParser(description='Create an AWS Lambda Deployment package or upload a package')
parser.add_argument('--build', action='store_true')
parser.add_argument('--deploy', action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    if args.build:
        build_lambda_zipfile()

    # (NEW_DEPLOYMENT_DIR, CURRENT_DEPLOYMENT_NAME) = make_deployment_dir()
    # copy_deployment_files(NEW_DEPLOYMENT_DIR, file_list)
    # copy_virtual_env_libs(NEW_DEPLOYMENT_DIR, "./venv")
    # new_deployment_zipfile_name = "deployments/{}.zip".format(CURRENT_DEPLOYMENT_NAME)
    # zipdir(NEW_DEPLOYMENT_DIR, new_deployment_zipfile_name)
    # copy_deployment_into_latest(new_deployment_zipfile_name)

    # print('Successfully created new deployment at {0:s} and {1:s}'.format(new_deployment_zipfile_name,
    else:
        # install_lambda_zipfile()
        print("Latest: {}".format(get_latest_deployment_directory()))
else:
    print("Error: intended to run locally")
    sys.exit(1)
