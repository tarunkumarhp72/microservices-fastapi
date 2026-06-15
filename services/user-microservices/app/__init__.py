from pathlib import Path
import sys


def _add_local_shared() -> None:
    for parent in Path(__file__).resolve().parents:
        shared_root = parent / "shared_lib"
        if shared_root.is_dir():
            sys.path.insert(0, str(shared_root))
            return


_add_local_shared()
