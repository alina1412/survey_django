import os

from django.conf import settings
from django.http import HttpResponse

BASE_DIR = settings.BASE_DIR


class AttachFile:
    def __init__(self, item_list):
        self.name = "download.txt"
        self.item_list = item_list
        dirname = BASE_DIR / "static/download/"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        self.fl_path = dirname / self.name

    def attach_file(self):
        self.create_file()
        return self.response_file_obj()

    def create_file(self):
        with open(self.fl_path, "w", encoding="utf-8") as file:
            for obj in self.item_list:
                line = " - ".join([obj.question])
                file.write(line)
                file.write(";\n")

    def response_file_obj(self):
        with open(self.fl_path, "rb") as file:
            content_type = "text/plain"
            # content_type, _ = mimetypes.guess_type(fl_path)
            # print(content_type)
            response = HttpResponse(file, content_type=content_type)
            response["Content-Disposition"] = f"attachment; filename={self.name}"
            return response

    def delete_file(self):
        ...

    # fl_path = f'{BASE_DIR}/static/img/{filename}'
    # print(fl_path)
