from dataclasses import dataclass
import json


@dataclass(init=True, repr=True, eq=True)
class DifferenceDTO:
    """
    A Data Transfer Object Class storing difference info
    """
    removed: str | None
    added: str | None
    index: int

    def __str__(self):
        return f"{self.index} -{self.removed or ''} +{self.added or ''}"

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__,
                          sort_keys=True, indent=4)


if __name__ == "__main__":
    pass
