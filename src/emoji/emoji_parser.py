from dataclasses import dataclass


@dataclass(slots=True)
class Emoji:
    emoji: str
    name: str
    version: str
    status: str
    group: str
    subgroup: str


class EmojiParser:

    def parse(self, filename: str):
        emojis = []

        group = ""
        subgroup = ""

        with open(filename, encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("# group:"):
                    group = line.removeprefix("# group:").strip()
                    continue

                if line.startswith("# subgroup:"):
                    subgroup = line.removeprefix("# subgroup:").strip()
                    continue

                if line.startswith("#"):
                    continue

                # Example:
                # 1F600 ; fully-qualified # 😀 E1.0 grinning face

                left, right = line.split("#", 1)

                _, status = left.split(";", 1)

                status = status.strip()

                parts = right.strip().split(maxsplit=2)

                emoji = parts[0]
                version = parts[1]
                name = parts[2]

                emojis.append(
                    Emoji(
                        emoji=emoji,
                        name=name,
                        version=version,
                        status=status,
                        group=group,
                        subgroup=subgroup,
                    )
                )

        return emojis
