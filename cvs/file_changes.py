import difflib
from cvs.data_transfer_object import DifferenceDTO


class FileChanges:
    # TODO make a good __str__ (all the inside, changed)
    """
    Stores all information about difference between two files
    """
    def __init__(self, prev_file_path: str = None,
                 curr_file_path: str = None):
        if prev_file_path is not None:
            with open(prev_file_path, 'r', encoding='utf-8') as f1:
                self.__file_lines_1 = f1.readlines()
        else:
            self.__file_lines_1 = []

        if curr_file_path is not None:
            with open(curr_file_path, 'r', encoding='utf-8') as f2:
                self.__file_lines_2 = f2.readlines()
        else:
            self.__file_lines_2 = []
        self.file_path = curr_file_path
        self.changes = self.find_difference(self.__file_lines_1,
                                            self.__file_lines_2)

    @staticmethod
    def find_difference(lines1, lines2):
        differ = difflib.Differ()
        differences = list(differ.compare(lines1, lines2))
        diff_counter = 0
        diff_started = False
        full_changes_dto = []
        filtered_differences = filter(lambda c: c[0] != "?", differences)
        for line in filtered_differences:
            if line[0] == "-":
                diff_started = True
                full_changes_dto.append(DifferenceDTO(removed=line[2:],
                                                      added=None,
                                                      index=diff_counter))
            elif line[0] == "+":
                if diff_started:
                    full_changes_dto[-1].added = line[2:]
                    diff_counter -= 1
                    diff_started = False
                else:
                    full_changes_dto.append(DifferenceDTO(removed=None,
                                                          added=line[2:],
                                                          index=diff_counter))
            diff_counter += 1
        
        return full_changes_dto
    
    def __eq__(self, other: "FileChanges"):
        return (self.__file_lines_1, self.__file_lines_2, self.changes) \
            == (other.__file_lines_1, other.__file_lines_2, other.changes)
    
    def __repr__(self):
        return f"FileChanges({self.__file_lines_1}, {self.__file_lines_2}):\n"\
               f" {self.changes})"

    def __str__(self):
        return "\n".join(str(d) for d in self.changes)
    
    
if __name__ == "__main__":
    pass
