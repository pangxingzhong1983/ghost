#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest configuration and shared fixtures
"""

import sys
import os
import pytest
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope='session')
def temp_dir():
    """临时目录 fixture"""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


@pytest.fixture
def temp_config_file(temp_dir):
    """临时配置文件 fixture"""
    config_path = os.path.join(temp_dir, 'test.conf')
    with open(config_path, 'w') as f:
        f.write("""
[paths]
prefer_workdir = true

[server]
host = 127.0.0.1
port = 8443

[security]
bind_password_min_length = 16
""")
    return config_path


@pytest.fixture(scope='function')
def mock_secretstorage(monkeypatch):
    """Mock secretstorage 模块（用于测试无该模块的环境）"""
    monkeypatch.setitem(sys.modules, 'secretstorage', None)
    yield
    # 恢复


@pytest.fixture(scope='function')
def mock_M2Crypto(monkeypatch):
    """Mock M2Crypto 模块"""
    class MockM2Crypto:
        pass

    monkeypatch.setitem(sys.modules, 'M2Crypto', MockM2Crypto)
    monkeypatch.setitem(sys.modules, 'M2Crypto', None)
    yield
    # 恢复


@pytest.fixture(autouse=True)
def setup_test_environment():
    """自动设置测试环境"""
    # 设置测试环境变量
    os.environ.setdefault('GHOST_TEST_ENV', 'true')
    yield
    # 清理
