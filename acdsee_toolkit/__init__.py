"""ACDSee Toolkit - Python library for image workflow automation."""

__version__ = "0.4.2"
__author__ = "ACDSee Toolkit Contributors"

from .scanner import LibraryScanner, ImageIndex
from .metadata import MetadataExtractor, ExifData

__all__ = [
    "LibraryScanner",
    "ImageIndex", 
    "MetadataExtractor",
    "ExifData",
    "__version__",
]
