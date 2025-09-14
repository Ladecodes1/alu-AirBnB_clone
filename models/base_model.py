#!/usr/bin/python3
"""BaseModel module: defines BaseModel class for AirBnB clone."""

from uuid import uuid4
from datetime import datetime

class BaseModel:
    """BaseModel that defines all common attributes/methods."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(value))
                elif key == "__class__":
                    continue
                else:
                    setattr(self, key, value)
            if not hasattr(self, "id"):
                self.id = str(uuid4())
            if not hasattr(self, "created_at"):
                self.created_at = datetime.now()
            if not hasattr(self, "updated_at"):
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # register in storage if available
            try:
                from models import storage
                storage.new(self)
            except Exception:
                pass

    def __str__(self):
        """Return string representation: [<class name>] (<id>) <__dict__>"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at and ask storage to persist."""
        self.updated_at = datetime.now()
        try:
            from models import storage
            storage.save()
        except Exception:
            pass

    def to_dict(self):
        """Return a dict representation with ISO datetime strings and __class__ name."""
        result = dict(self.__dict__)
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
        result["__class__"] = self.__class__.__name__
        return result
