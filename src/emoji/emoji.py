import json
from dataclasses import asdict

from emoji_parser import EmojiParser

print(f"Parsing emoji.txt...1")

parser = EmojiParser()

print(f"Parsing emoji.txt...2")

emojis = parser.parse("src/emoji/emoji.txt")
print(f"Parsed {len(emojis)} emojis")

with open("emoji.json", "w", encoding="utf-8") as f:
    json.dump(
        [asdict(e) for e in emojis],
        f,
        ensure_ascii=False,
        indent=2,
    )
