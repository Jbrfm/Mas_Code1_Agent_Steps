import csv
import io
import math
import re
import statistics
from collections import Counter


def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

def get_weather(city: str) -> str:
    """Return a mock current weather string for a city."""
    data = {"paris": "sunny, 22°C", "london": "rainy, 14°C"}
    return data.get(city.lower(), "unknown city")


def analyze_text(text: str, top_k: int = 5) -> dict:
    """Analyze Persian or English text: word/sentence counts and frequent words.

    Matching ignores case and normalizes Persian/Arabic variants of yeh and kaf.
    Words joined with a Persian half-space count as one word. Stopwords remain.
    top_k must be between 1 and 20. Input is limited to 100,000 characters.
    """
    if len(text) > 100_000:
        raise ValueError("Text must contain at most 100,000 characters.")
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20.")
    normalized = text.casefold().translate(str.maketrans({"ي": "ی", "ك": "ک"}))
    words = re.findall(r"[^\W_]+(?:\u200c[^\W_]+)*", normalized)
    sentences = [part for part in re.split(r"[.!?؟。]+", text) if re.search(r"\w", part)]
    return {
        "character_count": len(text),
        "word_count": len(words),
        "unique_word_count": len(set(words)),
        "sentence_count": len(sentences),
        "top_words": [
            {"word": word, "count": count}
            for word, count in Counter(words).most_common(top_k)
        ],
    }


def analyze_csv(csv_text: str) -> dict:
    """Analyze comma-separated CSV text with a header, without accessing files.

    Return row counts, missing cells and min/max/mean/median for columns whose
    nonempty cells are all finite numbers. Other columns are classified as text.
    Blank cells are missing values. Headers must be unique and nonempty; each
    row must have the same number of cells. Maximum input: 100,000 characters.
    """
    if len(csv_text) > 100_000:
        raise ValueError("CSV must contain at most 100,000 characters.")
    try:
        rows = list(csv.reader(io.StringIO(csv_text), strict=True))
    except csv.Error as exc:
        raise ValueError(f"Invalid CSV: {exc}") from exc
    rows = [row for row in rows if row]  # Ignore blank lines.
    if not rows:
        raise ValueError("CSV must include a header row.")
    headers = [cell.strip().lstrip("\ufeff") for cell in rows[0]]
    if not all(headers) or len(set(headers)) != len(headers):
        raise ValueError("CSV headers must be nonempty and unique.")
    if any(len(row) != len(headers) for row in rows[1:]):
        raise ValueError("Every CSV row must have the same number of cells as the header.")
    columns = {}
    for index, header in enumerate(headers):
        cells = [row[index].strip() for row in rows[1:]]
        populated = [cell for cell in cells if cell]
        summary = {"missing_count": len(cells) - len(populated), "type": "empty"}
        if populated:
            try:
                numbers = [float(cell) for cell in populated]
            except ValueError:
                numbers = []
            if numbers and all(math.isfinite(number) for number in numbers):
                summary.update(
                    type="numeric", min=min(numbers), max=max(numbers),
                    mean=statistics.mean(numbers), median=statistics.median(numbers),
                )
            else:
                summary["type"] = "text"
        columns[header] = summary
    return {"row_count": len(rows) - 1, "column_count": len(headers), "columns": columns}
