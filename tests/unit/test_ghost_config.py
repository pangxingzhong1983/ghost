#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for GhostConfig
"""

import pytest
import sys
import os
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def test_ghost_config_importable():
    """测试 GhostConfig 可导入"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig
        assert GhostConfig is not None
    except ImportError as e:
        pytest.fail(f"Failed to import GhostConfig: {e}")


def test_config_sections():
    """测试配置文件节的存在"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig
        # 创建临时配置避免使用真实配置
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[paths]
prefer_workdir = false

[server]
host = 0.0.0.0
port = 443
""")
            temp_config = f.name

        config = GhostConfig(temp_config)
        # 应该能读取 sections
        sections = config.sections()
        assert isinstance(sections, list)

        # 清理
        os.unlink(temp_config)
    except Exception as e:
        pytest.fail(f"Config test failed: {e}")


def test_config_get_boolean():
    """测试布尔值获取"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[test]
bool_true = true
bool_false = false
yes_value = yes
no_value = no
""")
            temp_config = f.name

        config = GhostConfig(temp_config)
        assert config.getboolean('test', 'bool_true') is True
        assert config.getboolean('test', 'bool_false') is False
        assert config.getboolean('test', 'yes_value') is True
        assert config.getboolean('test', 'no_value') is False

        os.unlink(temp_config)
    except Exception as e:
        pytest.fail(f"getboolean test failed: {e}")


def test_config_get_int():
    """测试整数值获取"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[test]
port = 443
max_connections = 100
""")
            temp_config = f.name

        config = GhostConfig(temp_config)
        assert config.getint('test', 'port') == 443
        assert config.getint('test', 'max_connections') == 100

        os.unlink(temp_config)
    except Exception as e:
        pytest.fail(f"getint test failed: {e}")


def test_config_get_folder():
    """测试文件夹路径获取"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[paths]
data = /tmp/ghost_data
""")
            temp_config = f.name

        config = GhostConfig(temp_config)
        # get_folder 应该创建目录（如果不存在）
        data_folder = config.get_folder('data', create=False)
        # 由于是 tempconfig，会返回绝对路径
        assert isinstance(data_folder, str)

        os.unlink(temp_config)
    except Exception as e:
        pytest.fail(f"get_folder test failed: {e}")


def test_pydantic_validation_integration():
    """测试 pydantic 验证集成（如果可用）"""
    try:
        from ghost.ghostlib.GhostConfig import GhostConfig, PYDANTIC_AVAILABLE
        if not PYDANTIC_AVAILABLE:
            pytest.skip("Pydantic not available")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[server]
host = 127.0.0.1
port = 8443
ssl = true

[security]
bind_password_min_length = 16
allow_default_credentials = false

[logging]
level = DEBUG
max_size_mb = 20

[network]
timeout = 30
""")
            temp_config = f.name

        config = GhostConfig(temp_config)
        # 如果 pydantic 可用，验证应该通过
        assert config.get('server', 'host') == '127.0.0.1'
        assert config.getint('server', 'port') == 8443

        # 验证 invalid port 会发出警告（但不抛出异常）
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
            f.write("""
[server]
port = 99999
""")
            bad_config = f.name

        # 应该能加载但验证会失败（记录 warning）
        config_bad = GhostConfig(bad_config)
        assert config_bad.getint('server', 'port') == 99999

        os.unlink(temp_config)
        os.unlink(bad_config)
    except Exception as e:
        pytest.fail(f"Pydantic integration test failed: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
