import os


def handle_uploaded_file(directory, file_name, file_obj):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print("directory does not exists")
            raise e

    file_path = "{directory}/{file_name}".format(
        directory=directory,
        file_name=file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
