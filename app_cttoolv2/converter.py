from pathlib import Path

from app_cttoolv2.filesystem import create_directory, untar_directory
# from app_cttoolv2.read_olx import OLXReader
# from app_cttoolv2.write_olx import compress_course


def convert_file(tar_file_path, temp_workspace):
    """
    Creates working directory in /tmp to unpack .tar.gz file.
    Inputs:
        tar_file_path: path to .tar.gz file.
        temp_workspace: path to temporary workspace.

    """
    create_directory(temp_workspace)
    untar_directory(tar_file_path, temp_workspace)

