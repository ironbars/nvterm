import os


class FileHandlerError(Exception):
    pass


class FileHandler(object):
    """
    Bridge between files and the text editor's buffer.
    """
    def __init__(self, filepath=None):
        self.filepath = filepath


    def read(self):
        if self.filepath is None:
            # New file
            return None

        with open(self.filepath, "r") as f:
            return f.read()


    def write(self, text):
        if self.filepath is None:
            raise FileHandlerError("Please supply a file name.")

        with open(self.filepath, "w") as f:
            f.write(text)
