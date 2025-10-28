from pathlib import Path
from typing import List


def get_data_folders() -> List[Path]:
    """Return existing data folders, supporting both 'data' and 'Data'.
    If neither exists, create lower-case 'data' and return it.
    """
    candidates = [Path("data"), Path("Data")]
    existing = [p for p in candidates if p.exists()]
    if not existing:
        candidates[0].mkdir(exist_ok=True)
        existing = [candidates[0]]
    return existing


def get_primary_data_folder() -> Path:
    """Return the primary data folder to use for writes (prefer 'data')."""
    folders = get_data_folders()
    for p in folders:
        if p.name == 'data':
            return p
    return folders[0]


def list_excel_files(include_xls: bool = True) -> List[Path]:
    """List Excel files across all data folders.
    include_xls: whether to include legacy .xls files
    """
    files: List[Path] = []
    seen = set()
    patterns = ["*.xlsx"] + (["*.xls"] if include_xls else [])
    for folder in get_data_folders():
        for pattern in patterns:
            for fp in folder.glob(pattern):
                key = str(fp.resolve())
                if key not in seen:
                    seen.add(key)
                    files.append(fp)
    return files
