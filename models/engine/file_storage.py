#!/usr/bin/python3
"""FileStorage engine: serializes instances to a JSON file and deserializes."""

import json
import os

class FileStorage:
    """Serializes instances to a JSON file and deserializes back to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add new object to __objects with key <class name>.<id>."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (using to_dict())."""
        obj_dict = {}
        for key, obj in FileStorage.__objects.items():
            try:
                obj_dict[key] = obj.to_dict()
            except Exception:
                continue
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize the JSON file to __objects, if the file exists."""
        if not os.path.exists(FileStorage.__file_path):
            return
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
            for key, val in obj_dict.items():
                cls_name = val.get("__class__")
                if not cls_name:
                    continue
                try:
                    module = __import__("models." + cls_name.lower(), fromlist=[cls_name])
                    cls = getattr(module, cls_name)
                    FileStorage.__objects[key] = cls(**val)
                except Exception:
                    # could not recreate the object (class file missing or  skiperror) 
                    continue
        except Exception:
            pass
