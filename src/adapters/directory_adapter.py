import os

from src.domain import file_port

_FOLDER: str = "src/adapters/videos/"

class DirectoryAdapter(file_port.FilePort):
    def _get_file(self, path) -> list[str]:
        files: list[str] = []
        new_path = os.path.abspath(path)
        for file_name in os.listdir(new_path):
            file_path = os.path.join(new_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".mkv"):
                files.append(file_path)

        return files

    def get_files(self) -> list[str]:
        return self._get_file(_FOLDER)

    def get_folder(self):
        return os.path.abspath(_FOLDER)