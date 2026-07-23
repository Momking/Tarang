from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FileInfo:
    path: Path
    name: str

    def to_dict(self):

        return {
            "path": str(self.path),
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            path=Path(data["path"]),
            name=data["name"],
        )
