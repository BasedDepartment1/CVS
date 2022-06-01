from cvs.file_changes import FileChanges
import json
import os.path


class Serializer:
    @staticmethod
    def serialize(changes, filename=None) -> str | None:
        changes = changes if isinstance(changes, dict) \
            else Serializer.make_dict(changes)
        if filename:
            with open(filename, "w") as f:
                json.dump(changes, fp=f, indent=4)
        else:
            return json.dumps(changes)

    @staticmethod
    def deserialize(json_data):
        method = json.load if os.path.exists(json_data) else json.loads
        return method(json_data)

    @staticmethod
    def make_dict(data: list):
        dictionary = dict()
        for point in data:
            if isinstance(point, FileChanges):
                dictionary[point.file_path] = tuple(map(str, point.changes))
            elif isinstance(point, tuple):
                dictionary[point[0]] = str(point[1])
            else:
                raise TypeError(f"Cannot serialize object "
                                f"of type: {point.__class__}")
        return dictionary

