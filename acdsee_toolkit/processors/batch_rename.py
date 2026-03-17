"""Batch renaming functionality."""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class RenameOperation:
    """A single rename operation."""
    source_path: Path
    target_path: Path
    source_name: str
    target_name: str


@dataclass
class RenamePlan:
    """Plan for batch rename operations."""
    operations: List[RenameOperation] = field(default_factory=list)
    
    def execute(self, dry_run: bool = False) -> int:
        """Execute all rename operations."""
        count = 0
        for op in self.operations:
            if not dry_run:
                op.source_path.rename(op.target_path)
            count += 1
        return count


class BatchRenamer:
    """Rename multiple files using a pattern."""
    
    def __init__(
        self,
        source_dir: str,
        pattern: str = "{date:%Y-%m-%d}_{index:04d}{ext}",
        dry_run: bool = True
    ):
        self.source_dir = Path(source_dir)
        self.pattern = pattern
        self.dry_run = dry_run
    
    def plan(self) -> RenamePlan:
        """Generate a rename plan."""
        plan = RenamePlan()
        
        if not self.source_dir.exists():
            return plan
        
        images = sorted(self.source_dir.glob("*"))
        images = [f for f in images if f.is_file() and f.suffix.lower() in 
                  {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}]
        
        for idx, img in enumerate(images, 1):
            stat = img.stat()
            date = datetime.fromtimestamp(stat.st_mtime)
            
            new_name = self.pattern.format(
                date=date,
                index=idx,
                ext=img.suffix,
                name=img.stem
            )
            
            new_path = self.source_dir / new_name
            
            plan.operations.append(RenameOperation(
                source_path=img,
                target_path=new_path,
                source_name=img.name,
                target_name=new_name
            ))
        
        return plan
