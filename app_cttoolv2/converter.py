from django.conf import settings

from app_cttoolv2.filesystem import create_directory, untar_directory
from app_cttoolv2.read_olx import OLXReader
from app_cttoolv2.write_olx import compress_course


def convert_file(tar_file_path, temp_workspace):
    """
    Creates working directory in /tmp to unpack .tar.gz file.
    Inputs:
        tar_file_path: path to .tar.gz file.
        temp_workspace: path to temporary workspace.

    """
    create_directory(temp_workspace)
    untar_directory(tar_file_path, temp_workspace)

    olx_reader = OLXReader()
    course_detail = olx_reader.traverse_workspace(
        temp_workspace
    )

    output_dir_path = settings.MEDIA_ROOT / 'output'
    if not output_dir_path.exists():
        create_directory(output_dir_path)

    new_file_path =  compress_course(course_detail['base_path'], course_detail['course_key_tags'])

    return {
        'new_file_path': new_file_path,
        'course_key_tags': course_detail['course_key_tags'],
        'info_context': course_detail['info_context']
    }
