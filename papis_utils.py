import os

class Document(object):

    """Class implementing the entry abstraction of a document in a library.
    It is basically a python dictionary with more methods.
    """

    subfolder = ""
    _infoFilePath = ""

    def __init__(self, folder=None, data=None):
        self._keys = []
        self._folder = None

        if folder is not None:
            self.set_folder(folder)
            self.load()

        if data is not None:
            self.update(data)

    def __delitem__(self, key):
        """Deletes property from document, e.g. ``del doc['url']``.
        :param key: Name of the property.
        :type  key: str
        """
        self._keys.pop(self._keys.index(key))
        delattr(self, key)

    def __setitem__(self, key, value):
        """Sets property to value from document, e.g. ``doc['url'] =
        'www.gnu.org'``.
        :param key: Name of the property.
        :type  key: str
        :param value: Value of the parameter
        :type  value: str,int,float,list
        """
        self._keys.append(key)
        setattr(self, key, value)

    def __getitem__(self, key):
        """Gets property to value from document, e.g. ``a = doc['url']``.
        If the property `key` does not exist, then the empy string is returned.

        :param key: Name of the property.
        :type  key: str
        :returns: Value of the property
        :rtype:  str,int,float,list
        """
        return getattr(self, key) if hasattr(self, key) else ""

    def get_main_folder(self):
        """Get full path for the folder where the document and the information
        is stored.
        :returns: Folder path
        """
        return self._folder

    def set_folder(self, folder):
        """Set document's folder. The info_file path will be accordingly set.

        :param folder: Folder where the document will be stored, full path.
        :type  folder: str
        """
        self._folder = folder
        self._infoFilePath = os.path.join(
            folder,
            "info.yaml"
            #papis.utils.get_info_file_name()
        )
        self.subfolder = self.get_main_folder()

    def get_main_folder_name(self):
        """Get main folder name where the document and the information is
        stored.
        :returns: Folder name
        """
        return os.path.basename(self._folder)

    def has(self, key):
        """Check if the information file has some key defined.

        :param key: Key name to be checked
        :returns: True/False
        """
        return key in self.keys()

    def check_files(self):
        """Check for the exsitence of the document's files
        :returns: False if some file does not exist, True otherwise
        :rtype:  bool
        """
        for f in self.get_files():
            # self.logger.debug(f)
            if not os.path.exists(f):
                print("** Error: %s not found in %s" % (
                    f, self.get_main_folder()))
                return False
            else:
                return True


    


    def get_info_file(self):
        """Get full path for the info file
        :returns: Full path for the info file
        :rtype: str
        """
        return self._infoFilePath

    def get_files(self):
        """Get the files linked to the document, if any.

        :returns: List of full file paths
        :rtype:  list
        """
        files = self["files"] if isinstance(self["files"], list) \
            else [self["files"]]
        result = []
        for f in files:
            result.append(os.path.join(self.get_main_folder(), f))
        return result

    def keys(self):
        """Returns the keys defined for the document.

        :returns: Keys for the document
        :rtype:  list
        """
        return self._keys

    def dump(self):
        """Return information string without any obvious format
        :returns: String with document's information
        :rtype:  str

        """
        string = ""
        for i in self.keys():
            string += str(i)+":   "+str(self[i])+"\n"
        return string

    def load(self):
        """Load information from info file
        """
        import yaml
        # TODO: think about if it's better to raise an exception here
        # TODO: if no info file is found
        try:
            fd = open(self.get_info_file(), "r")
        except:
            return False
        structure = yaml.load(fd)
        fd.close()
        for key in structure:
            self[key] = structure[key]