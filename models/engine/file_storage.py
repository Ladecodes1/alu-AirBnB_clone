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
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty file")
                obj_dict = json.loads(content)
            for key, val in obj_dict.items():
                cls_name = val.get("__class__")
                if not cls_name:
                    continue
                try:
                    if cls_name == "BaseModel":
                        from models.base_model import BaseModel
                        cls = BaseModel
                    elif cls_name == "User":
                        from models.user import User
                        cls = User
                    elif cls_name == "State":
                        from models.state import State
                        cls = State
                    elif cls_name == "City":
                        from models.city import City
                        cls = City
                    elif cls_name == "Amenity":
                        from models.amenity import Amenity
                        cls = Amenity
                    elif cls_name == "Place":
                        from models.place import Place
                        cls = Place
                    elif cls_name == "Review":
                        from models.review import Review
                        cls = Review
                    else:
                        continue
                    FileStorage.__objects[key] = cls(**val)
                except Exception:
                    # could not recreate the object (class file missing or error) 
                    continue
        except ValueError:
            raise
        except Exception:
            pass
