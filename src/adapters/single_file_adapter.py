from src.domain import file_port

_FOLDER: str = "../"

class SingleFileAdapter(file_port.FilePort):
    def _get_file(self, path: str) -> list[str]:
        return [f"{path}test.mkv"]

    def get_files(self) -> list[str]:
        return self._get_file(_FOLDER)

    def get_folder(self):
        return self._get_file(_FOLDER)