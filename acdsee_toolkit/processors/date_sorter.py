"""Sort images into date-based folders."""

import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SortResult:
    """Result of a sort operation."""
    moved_count: int = 0
    skipped_count: int = 0
    error_count: int = 0


class DateSorter:
    """Sort images into folders by date."""
    
    EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    
    def __init__(
        self,
        source_dir: str,
        dest_dir: str,
        folder_format: str = "%Y/%m-%B"
    ):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.folder_format = folder_format
    
    def run(self, copy: bool = False) -> SortResult:
        """Run the sort operation."""
        result = SortResult()
        
        if not self.source_dir.exists():
            return result
        
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        for item in self.source_dir.iterdir():
            if not item.is_file():
                continue
            if item.suffix.lower() not in self.EXTENSIONS:
                continue
            
            try:
                stat = item.stat()
                date = datetime.fromtimestamp(stat.st_mtime)
                folder_name = date.strftime(self.folder_format)
                
                target_folder = self.dest_dir / folder_name
                target_folder.mkdir(parents=True, exist_ok=True)
                
                target_path = target_folder / item.name
                
                if target_path.exists():
                    result.skipped_count += 1
                    continue
                
                if copy:
                    shutil.copy2(item, target_path)
                else:
                    shutil.move(str(item), str(target_path))
                
                result.moved_count += 1
                
            except Exception:
                result.error_count += 1
        
        return result
