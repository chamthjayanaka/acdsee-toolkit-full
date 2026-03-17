"""Library scanning and indexing functionality."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime


@dataclass
class ImageFile:
    """Represents a single image file in the library."""
    path: Path
    filename: str
    size_kb: float
    modified: datetime
    extension: str
    
    @classmethod
    def from_path(cls, path: Path) -> "ImageFile":
        stat = path.stat()
        return cls(
            path=path,
            filename=path.name,
            size_kb=stat.st_size / 1024,
            modified=datetime.fromtimestamp(stat.st_mtime),
            extension=path.suffix.lower()
        )


@dataclass
class FolderInfo:
    """Information about a scanned folder."""
    path: Path
    image_count: int = 0
    total_size_mb: float = 0.0


@dataclass
class ImageIndex:
    """Index of all images in a library."""
    images: List[ImageFile] = field(default_factory=list)
    folders: List[FolderInfo] = field(default_factory=list)
    
    @property
    def folder_count(self) -> int:
        return len(self.folders)
    
    def __len__(self) -> int:
        return len(self.images)


class ExtensionFilter:
    """Filter images by file extension."""
    
    def __init__(self, extensions: List[str]):
        self.extensions = {f".{ext.lower().lstrip('.')}" for ext in extensions}
    
    def matches(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions


class LibraryScanner:
    """Scan and index image directories."""
    
    DEFAULT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    
    def __init__(
        self,
        root_dir: str,
        filters: Optional[List[ExtensionFilter]] = None
    ):
        self.root_dir = Path(root_dir)
        self.filters = filters or []
        self._extensions = self.DEFAULT_EXTENSIONS.copy()
        
        for f in self.filters:
            if isinstance(f, ExtensionFilter):
                self._extensions = f.extensions
    
    def build_index(self, recursive: bool = True) -> ImageIndex:
        """Build an index of all images in the directory tree."""
        index = ImageIndex()
        
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.root_dir}")
        
        if recursive:
            for folder in self.root_dir.rglob("*"):
                if folder.is_dir():
                    self._scan_folder(folder, index)
            self._scan_folder(self.root_dir, index)
        else:
            self._scan_folder(self.root_dir, index)
        
        return index
    
    def _scan_folder(self, folder: Path, index: ImageIndex) -> None:
        """Scan a single folder for images."""
        folder_info = FolderInfo(path=folder)
        
        for item in folder.iterdir():
            if item.is_file() and item.suffix.lower() in self._extensions:
                try:
                    img = ImageFile.from_path(item)
                    index.images.append(img)
                    folder_info.image_count += 1
                    folder_info.total_size_mb += img.size_kb / 1024
                except (PermissionError, OSError):
                    continue
        
        if folder_info.image_count > 0:
            index.folders.append(folder_info)
