class DifferenceDTO:
    """
    A Data Transfer Object Class storing difference info
    """
    def __init__(self, removed: str | None, added: str | None, index: int):
        self.removed = removed
        self.added = added
        self.index = index

    def __eq__(self, other: "DifferenceDTO"):
        return self.removed == other.removed \
               and self.added == other.added \
               and self.index == other.index

    def __str__(self):
        return f"{self.index} - {self.removed}\n" \
               f"{len(str(self.index)) * ' '} + {self.added}"

    def __repr__(self):
        return f"DifferenceDTO({self.removed, self.added, self.index})"


if __name__ == "__main__":
    pass
