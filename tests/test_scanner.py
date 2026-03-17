"""Tests for LibraryScanner."""

import pytest
import tempfile
from pathlib import Path
from acdsee_toolkit import LibraryScanner


class TestLibraryScanner:
    """Test cases for LibraryScanner."""
    
    def test_scanner_init(self):
        """Test scanner initialization."""
        scanner = LibraryScanner(root_dir="/tmp")
        assert scanner.root_dir == Path("/tmp")
    
    def test_scan_empty_dir(self, tmp_path):
        """Test scanning an empty directory."""
        scanner = LibraryScanner(root_dir=str(tmp_path))
        index = scanner.build_index()
        assert len(index) == 0
    
    def test_scan_nonexistent_dir(self):
        """Test scanning a non-existent directory."""
        scanner = LibraryScanner(root_dir="/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            scanner.build_index()
