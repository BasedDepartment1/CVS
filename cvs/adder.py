import os
from cvs.file_changes import FileChanges
from cvs.init import Init
from cvs.directory_difference import DirectoryDifference, DiffKeys
from cvs.repository import Repository
from cvs.serializer import Serializer


class NotInitializedError(Exception):
    def __init__(self, msg: str):
        self.message = msg


class Adder:
    @staticmethod
    def add(path: str) -> None:
        """
        Adds a file or directory to the index

        :param path: path to file/directory
        :raises FileNotFoundError: if file/directory does
        not belong to repository
        :raises NotInitializedError: if repository was not set up
        """
        if Repository.cvs_dir is None:
            raise NotInitializedError
        try:
            if path != ".":
                os.path.relpath(path, Repository.worktree)
        except OSError:
            raise FileNotFoundError

        if path == ".":
            diff = Adder.__find_dir_difference(Repository.worktree)
        elif os.path.isdir(path):
            diff = Adder.__find_dir_difference(path)
        else:
            diff = Adder.__find_file_difference(path)

        if diff is not list:
            diff = [diff]
        Adder.__serialize_difference(diff)

    @staticmethod
    def __remove_dir_path(path: str) -> str:
        """
        Removes the full useless part of a path if it exists

        For example:
        We have set up repository in folder Slona:
        # Todo make test of it:
        C:/Users/Jopa/Slona/main.py -> Slona/main.py
        Slona/main.py -> Slona/main.py
        Slona\\main.py -> Slona/main.py

        :param path: path to file/directory to cut
        :return: relative path to file/directory
        """

        return os.path.relpath(path).replace("\\", "/")

    @staticmethod
    def __find_file_difference(path: str) -> FileChanges:
        """
        Finds difference between the current file and the file
        from index state folder
        :param path: path to current file
        :return: changes done to a file
        """
        return FileChanges.find_difference(Init.index_folder_path, path)

    @staticmethod
    def __find_dir_difference(path: str) -> list[FileChanges, tuple]:
        """
        Finds difference between current directory and directory
        from index state folder
        :param path: path to current directory
        :return: list of FileChanges for files and tuples
        (directory_path, DiffKeys.[difference type]) for directories
        """
        res = DirectoryDifference(Init.index_folder_path, path)
        changed_files = []

        for key, staged_change in res.changed_files:
            if key == DiffKeys.MODIFIED:
                changed_files \
                    .append(Adder.__find_file_difference(staged_change))
            else:
                changed_files.append((staged_change, key))

        return changed_files

    @staticmethod
    def __serialize_difference(
            differences: list[FileChanges, tuple[DiffKeys, list]]) -> None:
        """
        Add all calculated differences to .json file
        If file or directory difference exists, override it
        :param differences: differences between current and index state
        """
        path = os.path.join(Repository.cvs_dir, "index.json")
        previous = Serializer.deserialize(path)
        data = Adder.__intersect_difference(
            previous, Serializer.make_dict(differences))
        Serializer.serialize(data, path)

    @staticmethod
    def __intersect_difference(previous: dict, current: dict) -> dict:
        """
        Performs an intersection of already tracked file differences with
        freshly tracked ones
        :param previous: changes already added to
        :param current:
        :return:
        """
        for key in previous:
            if key not in current:
                current[key] = previous[key]
        return current
