import errno

from directory_difference import DirectoryDifference
import os
import shutil


class ChangeBuilder:
    def __init__(self, dir_to_change: str, changes: DirectoryDifference):
        self.prev_dir = dir_to_change.replace("\\", "/") \
            if dir_to_change[-1] in ["/", "\\"] \
            else dir_to_change.replace("\\", "/") + "/"

        self.changes = changes

    @staticmethod
    def __silent_remove(filename):
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def __delete_extra_files(self):
        files_to_delete = self.changes.changed_files["deleted"]
        for name in files_to_delete:
            full_path = self.prev_dir + name
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                self.__silent_remove(full_path)
        pass

    def __add_new_files(self):
        pass

    def __change_existent_files(self):
        pass

    def apply_changes(self):
        pass

