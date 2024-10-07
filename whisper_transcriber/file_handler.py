import os


class FileHandler:
    def __init__(self, file: bytes):
        self.file = file
        self.temp_file_path = "/tmp/uploaded_file"

        with open(self.temp_file_path, "wb") as f:
            f.write(file)

    def remove_temp_file(self):
        os.remove(self.temp_file_path)
