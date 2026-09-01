from dataclasses import dataclass
from pathlib import Path
import re
import yaml


@dataclass
class Chunk:
    filename: str
    heading: str
    text: str
    metadata: dict


def parse_file(path):
    text = path.read_text(encoding="utf-8")
    metadata = {}

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            metadata = yaml.safe_load(parts[1]) or {}
            text = parts[2]

    sections = re.split(r"(?=^##\s+)", text, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        first = section.splitlines()[0]

        heading = (
            first[3:].strip()
            if first.startswith("## ")
            else metadata.get("title", path.stem)
        )

        chunks.append(
            Chunk(
                filename=path.name,
                heading=heading,
                text=section,
                metadata=metadata.copy(),
            )
        )

    return chunks


def load_knowledge_base(path="knowledge-base"):
    chunks = []

    for file in sorted(Path(path).glob("*.md")):
        chunks.extend(parse_file(file))

    return chunks