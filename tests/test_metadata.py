"""Tests for MetadataExtractor."""

import pytest
from pathlib import Path
from acdsee_toolkit import MetadataExtractor


class TestMetadataExtractor:
    """Test cases for MetadataExtractor."""
    
    def test_extractor_init(self):
        """Test extractor initialization."""
        extractor = MetadataExtractor()
        assert extractor.include_fields is None
    
    def test_extractor_with_fields(self):
        """Test extractor with specific fields."""
        extractor = MetadataExtractor(include_fields=["Make", "Model"])
        assert "Make" in extractor.include_fields
        assert "Model" in extractor.include_fields
    
    def test_extract_nonexistent(self):
        """Test extracting from non-existent file."""
        extractor = MetadataExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.extract("/nonexistent/image.jpg")
