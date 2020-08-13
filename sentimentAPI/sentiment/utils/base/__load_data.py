#-*-coding:utf8-*-
"""
Load Data From File Or Path
"""
from __future__ import absolute_import

import pathlib
import os


def _load_file(filename, extension="", encoding="utf8"):
    """Load Data From File"""
    if isinstance(filename, str):
        if not os.path.exists(filename):
            raise f"File {filename} doesn't exit"

        with open(filename, "r") as file:
            return set(i.strip() for i in file.readline())
    elif isinstance(filename, (pathlib.PosixPath, pathlib.WindowsPath)):
        if filename.name.endswith(extension):
            return set(filename.read_text(encoding=encoding).split("\n"))


def _load_mapping_data(filename, extension="", encoding="utf8"):
    """Load Mapping Data"""
    if isinstance(filename, str):
        if not os.path.exists(filename):
            raise f"File {filename} doesn't exit"

        with open(filename, "r", encoding=encoding) as file:
            result = {}
            for line in file.readlines():
                if line.strip():
                    words = line.split(" ")
                    result[words[0]] = words[1].strip()

        return result
    elif isinstance(filename, (pathlib.PosixPath, pathlib.WindowsPath)):
        if filename.name.endswith(extension):
            result = {}
            for line in set(filename.read_text(encoding=encoding).split("\n")):
                if line.strip():
                    words = line.split(" ")
                    result[words[0]] = words[1].strip()
            return result
    else:
        raise TypeError("Missing a file path string")


def _load_from_path(path, extension="", recursive=False, encoding="utf8", mapping=False):
    """Load Data From Path
    
    Load data from specified path, if choose recurcive option, then can go deep 
    directory.
    
    Args:
    ---------
    path: string with directory, can use relative path or absolute path
    extension: file extension name, if space, load all file, otherwise get the
        unique file
    recursive: boolean, choose whether dive into directory
    encoding: file encoding
    mapping: boolean, load dict data

    Results:
    --------
    Store the item as set or dict

    Examples:
    -----------
    >>> data = _load_from_path(".", recursive=True, extension="txt")
    >>> data = _load_from_path(".")
    """
    if mapping:
        func = _load_mapping_data
        result = {} 
    else:
        func = _load_file # choose function
        result = set()

    for filepath in pathlib.Path(path).iterdir():
        if filepath.is_file():
            data = func(filepath, extension, encoding)
            if data:
                result.update(data)
        elif recursive and filepath.is_dir():
            result.update(_load_from_path(filepath, extension, recursive, encoding))

    return result





__all__ = ["_load_file", "_load_from_path", "_load_mapping_data"]