import abc

class FilePort(abc.ABC):
    @abc.abstractmethod
    def get_files(self):
        pass

    @abc.abstractmethod
    def _get_file(self, path):
        pass