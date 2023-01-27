from typing import List
from pathlib import PureWindowsPath

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

SEP = "\\"


class DirectoryTree:
    drives: List[str]

    def __init__(self):
        self.drives = []

    def add_unc(self, path: str):
        path_ = PureWindowsPath(path)
        self.add_drive(path_.drive)

    def add_drive(self, drive: str):
        if drive not in self.drives:
            self.drives.append(drive)

    def generate(self):
        #tree = self._generator.build_tree()
        #for entry in tree:
        #    print(entry)
        pass


class _TreeGenerator:
    def __init__(self, root_dir):
        self._root_dir = root_dir
        self._tree = []

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{SEP}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry_: entry_.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(
            self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}{SEP}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")
