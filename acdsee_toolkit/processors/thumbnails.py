"""Thumbnail generation."""

from pathlib import Path
from dataclasses import dataclass
from typing import Tuple
import time

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@dataclass
class ThumbnailResult:
    """Result of thumbnail generation."""
    success_count: int = 0
    skip_count: int = 0
    error_count: int = 0
    elapsed: float = 0.0


class ThumbnailGenerator:
    """Generate thumbnails for images."""
    
    EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    
    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        size: Tuple[int, int] = (256, 256),
        format: str = "JPEG",
        quality: int = 85
    ):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.size = size
        self.format = format
        self.quality = quality
        
        if not HAS_PIL:
            raise ImportError("Pillow is required. Install with: pip install Pillow")
    
    def run(self) -> ThumbnailResult:
        """Generate thumbnails for all images."""
        start = time.time()
        result = ThumbnailResult()
        
        if not self.source_dir.exists():
            return result
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        for item in self.source_dir.rglob("*"):
            if not item.is_file():
                continue
            if item.suffix.lower() not in self.EXTENSIONS:
                continue
            
            relative = item.relative_to(self.source_dir)
            output_path = self.output_dir / relative.with_suffix(".jpg")
            
            if output_path.exists():
                result.skip_count += 1
                continue
            
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with Image.open(item) as img:
                    img.thumbnail(self.size, Image.Resampling.LANCZOS)
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    img.save(output_path, self.format, quality=self.quality)
                
                result.success_count += 1
                
            except Exception:
                result.error_count += 1
        
        result.elapsed = time.time() - start
        return result
