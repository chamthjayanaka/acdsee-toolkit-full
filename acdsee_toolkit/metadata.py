"""Metadata extraction from image files."""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@dataclass
class ExifData:
    """Container for EXIF metadata."""
    raw: Dict[str, Any] = field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)
    
    def __contains__(self, key: str) -> bool:
        return key in self.raw


@dataclass
class ImageMetadata:
    """Complete metadata for an image file."""
    path: Path
    exif: ExifData = field(default_factory=ExifData)
    width: int = 0
    height: int = 0
    format: str = ""
    has_gps: bool = False
    
    @property
    def resolution(self) -> str:
        return f"{self.width}x{self.height}"


class MetadataExtractor:
    """Extract metadata from image files."""
    
    def __init__(self, include_fields: Optional[List[str]] = None):
        self.include_fields = set(include_fields) if include_fields else None
        
        if not HAS_PIL:
            raise ImportError("Pillow is required for metadata extraction. Install with: pip install Pillow")
    
    def extract(self, path: str | Path) -> ImageMetadata:
        """Extract metadata from a single image file."""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        
        metadata = ImageMetadata(path=path)
        
        try:
            with Image.open(path) as img:
                metadata.width = img.width
                metadata.height = img.height
                metadata.format = img.format or ""
                
                exif_data = {}
                raw_exif = img._getexif()
                
                if raw_exif:
                    for tag_id, value in raw_exif.items():
                        tag_name = TAGS.get(tag_id, str(tag_id))
                        
                        if self.include_fields and tag_name not in self.include_fields:
                            continue
                        
                        if isinstance(value, bytes):
                            try:
                                value = value.decode("utf-8", errors="ignore")
                            except:
                                value = str(value)
                        
                        exif_data[tag_name] = value
                        
                        if tag_name == "GPSInfo":
                            metadata.has_gps = True
                
                metadata.exif = ExifData(raw=exif_data)
        
        except Exception as e:
            pass
        
        return metadata
    
    def extract_batch(self, paths: List[Path]) -> List[ImageMetadata]:
        """Extract metadata from multiple images."""
        results = []
        for path in paths:
            try:
                results.append(self.extract(path))
            except Exception:
                continue
        return results
