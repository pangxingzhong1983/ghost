#!/usr/bin/env python3
"""
Unit test for GhostConfig class
"""

import os
import tempfile
import shutil
from ghost.ghostlib.GhostConfig import GhostConfig

def test_config_creation():
    """Test creating a new config file"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Use the default config name
        test_config = 'ghost.conf'
        
        # Create a GhostConfig instance
        config = GhostConfig(test_config)
        
        # Test adding a section and option
        if not config.has_section('test'):
            config.add_section('test')
        config.set('test', 'key', 'value')
        
        # Test getting the value
        assert config.get('test', 'key') == 'value', "Config value not set correctly"
        
        # Test saving the config
        config.save()
        
        # Test loading the config again
        new_config = GhostConfig(test_config)
        assert new_config.get('test', 'key') == 'value', "Config not saved correctly"
        
        print("✓ Config creation test passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def test_tags_functionality():
    """Test tags functionality"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a test config file
        test_config = os.path.join(temp_dir, 'test.conf')
        
        # Create a GhostConfig instance
        config = GhostConfig(test_config)
        
        # Test tags for a node
        tags = config.tags('test-node')
        
        # Test adding tags
        tags.add('tag1', 'tag2')
        assert 'tag1' in tags.get(), "Tag1 not added"
        assert 'tag2' in tags.get(), "Tag2 not added"
        
        # Test removing a tag
        tags.remove('tag1')
        assert 'tag1' not in tags.get(), "Tag1 not removed"
        assert 'tag2' in tags.get(), "Tag2 should still be present"
        
        # Test clearing tags
        tags.clear()
        assert len(tags.get()) == 0, "Tags not cleared"
        
        print("✓ Tags functionality test passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def test_get_path():
    """Test get_path method"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a test config file
        test_config = os.path.join(temp_dir, 'test.conf')
        
        # Create a GhostConfig instance
        config = GhostConfig(test_config)
        
        # Test getting a path
        test_path = config.get_path('test.txt', create=True)
        assert os.path.exists(os.path.dirname(test_path)), "Directory not created"
        
        print("✓ get_path method test passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    print("Running GhostConfig unit tests...")
    test_config_creation()
    test_tags_functionality()
    test_get_path()
    print("All tests passed!")