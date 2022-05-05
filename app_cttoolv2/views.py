import json
import tarfile
import tempfile
import traceback

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path

from app_cttoolv2.converter import convert_file


def index(request):
    context = {}
    return render(request, 'index.html', context)


def convert_course(request):
    context = {}
    tar_file = request.FILES.get('input-file')

    settings.ENV_NAME = request.POST.get('env','DEV')
    source_file_name = default_storage.save(tar_file.name, ContentFile(tar_file.read()))

    new_file_metadata = process_tar_file(source_file_name)
    default_storage.delete(source_file_name)

    response = HttpResponse(json.dumps(new_file_metadata))
    return response


def process_tar_file(source_file_name):
    source_file_path = settings.MEDIA_ROOT / source_file_name

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_workspace = Path(tmpdirname) / settings.WORKSPACE.stem
        for input_tar_file in _get_files(source_file_path):
            try:
                return convert_file(input_tar_file, temp_workspace)
            except Exception:
                traceback.print_exc()


def _is_tar_file(path):
    return path.is_file() and path.suffix == settings.TAR_FILE_EXTENSION


def _get_files(path):
    files = set()

    if not path.exists():
        raise FileNotFoundError
    if _is_tar_file(path):
        files.add(path)

    if path.is_dir():
        for input_file in path.iterdir():
            if _is_tar_file(input_file):
                files.add(input_file)

    return files
