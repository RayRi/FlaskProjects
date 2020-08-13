#coding:utf8
"""
The script is used to create base class to deal with data:
* FileHandler: Handle file
"""



class FileHanler:
    """File Context Manager

    File handler with context manger, there are two options to extract file text:
    1. use a reader method that is generator function
    2. use `with` context manager to extract file line, which can be extended

    Method:
        reader: generator function that yields a line
    """
    __slots__ = ["__file", "__options", "__handler"]

    def __init__(self, filename, **kwargs):
        self.__file = filename
        self.__options = kwargs


    def reader(self):
        """File Line Generator"""
        with self as file:
            line = file.readline()
            while line:
                yield line
                line = file.readline()


    def __enter__(self):
        self.__handler = open(self.__file, **self.__options)
        return self.__handler

    
    def __exit__(self, exc_type, exc_val, traceback):
        self.__handler.close()


    def __repr__(self):
        id_ = hex(id(self))
        return f"<{self.__class__.__name__} at {id_}>"


