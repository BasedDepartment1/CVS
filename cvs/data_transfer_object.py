from dataclasses import dataclass
import json


@dataclass(init=True, repr=True, eq=True, kw_only=True)
class DifferenceDTO:
    """
    A Data Transfer Object Class storing difference info
    """
    index: int
    removed: str | None
    added: str | None

    def __str__(self):
        return f"{self.index} -{self.removed or ''} +{self.added or ''}"

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def parse(line: str) -> "DifferenceDTO":
        components = line.split()
        return DifferenceDTO(int(components[0]),
                             components[1][1:], components[2][1:])


if __name__ == "__main__":
    pass
