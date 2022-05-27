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
    initialized = False

    initial_folder_name = "initial_state"
    index_folder_name = "index_state"

    @staticmethod
    def initialize():
        cur_dir = os.getcwd()
        rep_path = f"{cur_dir}/.cvs"

        try:
            pathlib.Path(rep_path).mkdir(parents=True)
        except FileExistsError:
            raise InitializationException("Repository was already initialized")

        Init.__make_directory_image(
            cur_dir, f"{rep_path}/{Init.initial_folder_name}")
        Init.__make_directory_image(
            cur_dir, f"{rep_path}/{Init.index_folder_name}")

        Init.initialized = True

    @staticmethod
    def __make_directory_image(cur_path: str, path: str):
        ignore_rep = shutil.ignore_patterns(f".cvs")
        shutil.copytree(cur_path, path, ignore=ignore_rep)


if __name__ == "__main__":
    Init.initialize()
