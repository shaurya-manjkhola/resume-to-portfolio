import os
import re
import json
import random
from typing import Optional

# Flat-file persistence: one JSON file per shareable portfolio link.
# Deliberately not a full database — no accounts, no auth, no editing.
# Each file stores exactly what's needed to re-render the chosen theme
# from the already-structured profile, rather than storing raw HTML,
# so links stay consistent with whatever the renderer currently does.
STORAGE_DIR = "portfolios"
os.makedirs(STORAGE_DIR, exist_ok=True)


def _slugify(name: str) -> str:
    """
    Turns a person's name into a URL-safe slug.
    'Parshav Giya' -> 'parshav-giya'
    """
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "portfolio"


def _path_for(slug: str) -> str:
    return os.path.join(STORAGE_DIR, f"{slug}.json")


def generate_slug(name: str) -> str:
    """
    Builds a slug from a person's name. If that slug is already taken
    (e.g. two people named 'Aryan Mehta'), appends a random 4-digit
    suffix and retries until a free slug is found.
    """
    base_slug = _slugify(name)
    slug = base_slug
    attempts = 0
    while os.path.exists(_path_for(slug)) and attempts < 20:
        slug = f"{base_slug}-{random.randint(1000, 9999)}"
        attempts += 1
    return slug


def save_portfolio(slug: str, profile_dict: dict, theme: str) -> None:
    """
    Persists a chosen profile + theme under a slug so it can be
    revisited later at a stable link, rather than only existing as
    a one-off response.
    """
    payload = {"profile": profile_dict, "theme": theme}
    with open(_path_for(slug), "w") as f:
        json.dump(payload, f)


def load_portfolio(slug: str) -> Optional[dict]:
    """
    Loads a previously saved {profile, theme} record, or None if
    no portfolio exists at that slug.
    """
    path = _path_for(slug)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)