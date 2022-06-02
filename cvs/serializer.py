from file_changes import FileChanges
import json
import os.path


class Serializer:
    @staticmethod
    def serialize(changes, filename) -> None:
        changes = changes if isinstance(changes, dict) \
            else Serializer.make_dict(changes)

        with open(filename, "w+") as f:
            json.dump(changes, fp=f, indent=4)

    @staticmethod
    def deserialize(json_data):
        # method = json.load if os.path.exists(json_data) else json.loads
        # return method(json_data)
        with open(json_data) as f:
            if f.read() == "":
                return dict()
            return json.load(f)

    @staticmethod
    def make_dict(data: list):
        dictionary = dict()
        print(data)
        for point in data:
            if isinstance(point, FileChanges):
                dictionary[point.file_path] = tuple(map(str, point.changes))
            elif isinstance(point, tuple):
                dictionary[point[0]] = str(point[1])
            else:
                raise TypeError(f"Cannot serialize object "
                                f"of type: {point.__class__}")
        return dictionary

