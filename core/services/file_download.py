import base64
from django.http import HttpResponse


def download_file(file_name, file_path, extension):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        file_content = base64.b64decode(encoded_string)
        file_content_type = "application/{ext}".format(ext=extension)
        response = HttpResponse(file_content, content_type=file_content_type)
        response['Content-Disposition'] = "attachment; filename=\"{filename}\"".format(filename=file_name)
        return response
