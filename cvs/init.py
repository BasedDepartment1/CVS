import os
import shutil
import pathlib


class InitializationException(Exception):
    def __init__(self, message: str):
        self.msg = message


class Init:
    """
    Initializes repository on current path
    """
    rep_path: str
    initial_folder_path: str
    index_folder_path: str
    initialized = False

    __initial_folder_name = "initial_state"
    __index_folder_name = "index_state"

    @staticmethod
    def initialize():
        cur_dir = os.getcwd()
        rep_path = f"{cur_dir}/.cvs"

        try:
            pathlib.Path(rep_path).mkdir(parents=True)
        except FileExistsError:
            raise InitializationException("Repository was already initialized")

        Init.initial_folder_path = f"{rep_path}/{Init.__initial_folder_name}"
        Init.index_folder_path = f"{rep_path}/{Init.__index_folder_name}"

        Init.__make_directory_image(
            cur_dir, Init.initial_folder_path)
        Init.__make_directory_image(
            cur_dir, Init.index_folder_path)

        Init.initialized = True

    @staticmethod
    def __make_directory_image(cur_path: str, path: str):
        ignore_rep = shutil.ignore_patterns(f".cvs")
        shutil.copytree(cur_path, path, ignore=ignore_rep)


if __name__ == "__main__":
    Init.initialize()
