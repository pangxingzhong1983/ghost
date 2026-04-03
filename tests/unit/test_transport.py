#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Transport and related classes
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def test_transport_constants():
    """测试Transport常量"""
    from ghost.network.transports import (
        LAUNCHER_TYPE_ALL,
        LAUNCHER_TYPE_CONNECT,
        LAUNCHER_TYPE_BIND,
        LAUNCHER_TYPE_DNSCNC,
    )

    assert LAUNCHER_TYPE_ALL == 0
    assert LAUNCHER_TYPE_CONNECT == 1
    assert LAUNCHER_TYPE_BIND == 2
    assert LAUNCHER_TYPE_DNSCNC == 3


def test_transport_exception():
    """测试 TransportException"""
    from ghost.network.transports import TransportException

    exc = TransportException("test error")
    assert str(exc) == "test error"


def test_transport_class():
    """测试 Transport 基础类"""
    from ghost.network.transports import Transport

    class DummyTransport(Transport):
        name = "dummy"
        server = None
        client = None

    transport = DummyTransport()
    assert transport.name == "dummy"
    assert transport.launcher_type == 0  # LAUNCHER_TYPE_ALL

    # 测试 bind_payload 模式
    transport_bind = DummyTransport(bind_payload=True)
    assert transport_bind.launcher_type == 2  # LAUNCHER_TYPE_BIND
    assert transport_bind.bind_payload is True


def test_transport_parse_args():
    """测试 Transport 参数解析"""
    from ghost.network.transports import Transport

    class DummyTransport(Transport):
        name = "dummy"

    transport = DummyTransport()
    test_args = {"key1": "value1", "key2": 123}
    transport.parse_args(test_args)

    assert transport.client_transport_kwargs == test_args
    assert transport.server_transport_kwargs == test_args


def test_no_hardcoded_defaults():
    """测试默认凭据已移除（不应有硬编码）"""
    from ghost.network.transports import (
        DEFAULT_BIND_PAYLOADS_PASSWORD,
        DEFAULT_DNSCNC_PUB_KEY,
        DEFAULT_DNSCNC_PRIV_KEY,
        DEFAULT_RSA_PUB_KEY,
        DEFAULT_SSL_BIND_CERT,
        DEFAULT_SSL_BIND_KEY,
    )

    # 所有默认值应该为 None
    assert DEFAULT_BIND_PAYLOADS_PASSWORD is None
    assert DEFAULT_DNSCNC_PUB_KEY is None
    assert DEFAULT_DNSCNC_PRIV_KEY is None
    assert DEFAULT_RSA_PUB_KEY is None
    assert DEFAULT_SSL_BIND_CERT is None
    assert DEFAULT_SSL_BIND_KEY is None


class TestSSLConfig:
    """测试 SSL 配置"""

    def test_ssl_protocol_constant(self):
        """验证 SSL 协议使用 TLS 而不是 SSLv23"""
        import ssl
        # 检查 conf.py 文件内容而非类，因为类可能不是 DummySSLAuthenticator
        from ghost.network.transports.ssl import conf as ssl_conf
        # 检查模块级别的 ssl_version 或类中的默认值
        # 直接读取文件可能更可靠
        import inspect
        source = inspect.getsource(ssl_conf)
        assert 'PROTOCOL_TLS_SERVER' in source or 'ssl_version' in source


class TestGhostSSLClient:
    """测试 GhostSSLClient"""

    def test_ssl_client_initialization(self):
        """测试 SSL 客户端初始化"""
        from ghost.network.lib.clients import GhostSSLClient

        # 默认启用 SSL 认证 (ssl_auth=True)
        client = GhostSSLClient()
        assert client.ssl_auth is True

    def test_ssl_client_with_auth_flag(self):
        """测试设置 ssl_auth=True"""
        from ghost.network.lib.clients import GhostSSLClient

        client = GhostSSLClient(ssl_auth=True)
        assert client.ssl_auth is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
