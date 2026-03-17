"""Duplicate image detection using perceptual hashing."""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict

try:
    import imagehash
    from PIL import Image
    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False


@dataclass
class DuplicateImage:
    """An image identified as a duplicate."""
    path: Path
    size_kb: float
    hash_value: str


class DuplicateFinder:
    """Find duplicate images using perceptual hashing."""
    
    EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    
    def __init__(
        self,
        directory: str,
        method: str = "phash",
        threshold: int = 8
    ):
        self.directory = Path(directory)
        self.method = method
        self.threshold = threshold
        
        if not HAS_IMAGEHASH:
            raise ImportError(
                "imagehash is required. Install with: pip install imagehash"
            )
    
    def _compute_hash(self, path: Path) -> str:
        """Compute perceptual hash for an image."""
        with Image.open(path) as img:
            if self.method == "phash":
                h = imagehash.phash(img)
            elif self.method == "dhash":
                h = imagehash.dhash(img)
            elif self.method == "ahash":
                h = imagehash.average_hash(img)
            else:
                h = imagehash.phash(img)
            return str(h)
    
    def find(self) -> List[List[DuplicateImage]]:
        """Find duplicate images in the directory."""
        if not self.directory.exists():
            return []
        
        hashes: Dict[str, List[DuplicateImage]] = defaultdict(list)
        
        for item in self.directory.rglob("*"):
            if not item.is_file():
                continue
            if item.suffix.lower() not in self.EXTENSIONS:
                continue
            
            try:
                hash_value = self._compute_hash(item)
                stat = item.stat()
                
                dup = DuplicateImage(
                    path=item,
                    size_kb=stat.st_size / 1024,
                    hash_value=hash_value
                )
                hashes[hash_value].append(dup)
                
            except Exception:
                continue
        
        duplicates = [group for group in hashes.values() if len(group) > 1]
        return duplicates
