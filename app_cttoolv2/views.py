from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import tarfile


def index(request):
    context = {}
    return render(request, 'index.html', context)

def convert_course(request):
    context = {}
    tar_file = request.FILES.get('input-file')

    path = default_storage.save(tar_file.name, ContentFile(tar_file.read()))

    tar = tarfile.open(path, "r:gz")
    my_file = tar.fileobj

    response = HttpResponse(my_file, content_type=tar_file.content_type)
    return response

