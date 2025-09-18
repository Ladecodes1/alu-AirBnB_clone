#!/usr/bin/python3
"""Review model."""
from models.base_model import BaseModel

class Review(BaseModel):
    """Review for AirBnB."""
    place_id = ""
    user_id = ""
    text = ""
