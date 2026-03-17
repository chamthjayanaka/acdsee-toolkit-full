"""Tests for processors."""

import pytest
from pathlib import Path
from acdsee_toolkit.processors import BatchRenamer, DateSorter


class TestBatchRenamer:
    """Test cases for BatchRenamer."""
    
    def test_renamer_init(self, tmp_path):
        """Test renamer initialization."""
        renamer = BatchRenamer(source_dir=str(tmp_path))
        assert renamer.source_dir == tmp_path
        assert renamer.dry_run is True
    
    def test_plan_empty_dir(self, tmp_path):
        """Test planning on empty directory."""
        renamer = BatchRenamer(source_dir=str(tmp_path))
        plan = renamer.plan()
        assert len(plan.operations) == 0


class TestDateSorter:
    """Test cases for DateSorter."""
    
    def test_sorter_init(self, tmp_path):
        """Test sorter initialization."""
        dest = tmp_path / "dest"
        sorter = DateSorter(
            source_dir=str(tmp_path),
            dest_dir=str(dest)
        )
        assert sorter.source_dir == tmp_path
    
    def test_sort_empty_dir(self, tmp_path):
        """Test sorting an empty directory."""
        dest = tmp_path / "dest"
        sorter = DateSorter(
            source_dir=str(tmp_path),
            dest_dir=str(dest)
        )
        result = sorter.run()
        assert result.moved_count == 0
