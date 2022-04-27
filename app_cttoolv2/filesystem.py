import json
import logging
import shutil
import tarfile
import traceback

from django.conf import settings

logger = logging.getLogger()


def create_directory(directory_path):
    """
    Removes the output directory if it exists and then creates it.
    This is so as not to have files
    from a previous run confusing the output.
    Inputs:
        directory_path: Path object of directory which needs to be created.
    """
    if directory_path.exists() and directory_path.is_dir():
        shutil.rmtree(str(directory_path))

    directory_path.mkdir()
    logger.debug("Created the folder: %s", directory_path)


def untar_directory(path_src, path_dst_base=None):
    """
    Decompresses given tar file.
    Inputs:
        path_src: path to .tar.gz file.
        path_dst_base: path to temporary workspace.
    """
    src_dir_path = path_src.parent
    path_dst_base = path_dst_base or src_dir_path

    path_dst = path_dst_base / path_src.with_suffix('').stem

    with tarfile.open(str(path_src)) as tar_file:
        tar_file.extractall(str(path_dst))

    return path_dst

def get_configuration():
    """
    Returns JSON object as a dictionary.
    """
    try:
        with open(settings.CONFIG_PATH, encoding='utf-8') as conf_file:
            conf_json = json.load(conf_file)
    except Exception:
        traceback.print_exc()

    return conf_json.get(settings.ENV_NAME)
