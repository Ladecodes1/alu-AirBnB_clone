#!/usr/bin/python3
"""This module instantiates the storage object used by the models package."""

import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# load existing objects from file (if any)
storage.reload()
