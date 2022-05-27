from dataclasses import dataclass


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


if __name__ == "__main__":
    pass
