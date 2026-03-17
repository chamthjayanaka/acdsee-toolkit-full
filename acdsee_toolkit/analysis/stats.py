"""Library statistics and reporting."""

from dataclasses import dataclass
from typing import Dict, Optional
from collections import Counter


@dataclass
class LibraryReport:
    """Statistics report for an image library."""
    total_images: int = 0
    total_size_gb: float = 0.0
    unique_cameras: int = 0
    date_range: str = ""
    top_extension: str = ""
    top_extension_pct: float = 0.0
    folders_scanned: int = 0
    
    def summary(self) -> str:
        """Generate a formatted summary string."""
        lines = [
            "─" * 45,
            "ACDSee Toolkit — Library Report",
            "─" * 45,
            f"Total images    : {self.total_images:,}",
            f"Total size      : {self.total_size_gb:.1f} GB",
            f"Unique cameras  : {self.unique_cameras}",
            f"Date range      : {self.date_range}",
            f"Top extension   : {self.top_extension} ({self.top_extension_pct:.1f}%)",
            f"Folders scanned : {self.folders_scanned}",
            "─" * 45,
        ]
        return "\n".join(lines)


class LibraryStats:
    """Generate statistics for an image library."""
    
    def __init__(self, library):
        self.library = library
    
    def generate(self) -> LibraryReport:
        """Generate a statistics report."""
        report = LibraryReport()
        
        report.total_images = len(self.library.images)
        report.folders_scanned = self.library.folder_count
        
        if not self.library.images:
            return report
        
        total_kb = sum(img.size_kb for img in self.library.images)
        report.total_size_gb = total_kb / (1024 * 1024)
        
        extensions = Counter(img.extension for img in self.library.images)
        if extensions:
            top_ext, top_count = extensions.most_common(1)[0]
            report.top_extension = top_ext
            report.top_extension_pct = (top_count / report.total_images) * 100
        
        dates = [img.modified for img in self.library.images]
        if dates:
            min_date = min(dates).strftime("%Y-%m-%d")
            max_date = max(dates).strftime("%Y-%m-%d")
            report.date_range = f"{min_date} → {max_date}"
        
        return report
