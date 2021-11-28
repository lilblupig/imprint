"""
    Imprint Nov 2021
    Cloudinary configuration for image management
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name=os.environ.get("CLOUD_NAME"),
  api_key=os.environ.get("API_KEY"),
  api_secret=os.environ.get("API_SECRET")
)
