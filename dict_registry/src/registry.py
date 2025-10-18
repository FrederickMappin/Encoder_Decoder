class DictionaryRegistry:
    def __init__(self):
        self._dictionaries = {}

    def _process_dictionary(self, dictionary):
        """
        Reverse the dictionary, shift values up by 1, and add {null: 0}.
        """
        processed_dict = {v: k + 1 for k, v in dictionary.items()}
        processed_dict["null"] = 0
        return processed_dict

    def register_dictionary(self, name, dictionary):
        """
        Register a dictionary after processing it.
        """
        if name in self._dictionaries:
            raise ValueError(f"Dictionary '{name}' is already registered.")
        processed_dict = self._process_dictionary(dictionary)
        self._dictionaries[name] = processed_dict

    def get_dictionary(self, name):
        """
        Retrieve a processed dictionary by name.
        """
        if name not in self._dictionaries:
            raise KeyError(f"Dictionary '{name}' not found.")
        return self._dictionaries[name]

    def list_dictionaries(self):
        """
        List all registered dictionary names.
        """
        return list(self._dictionaries.keys())