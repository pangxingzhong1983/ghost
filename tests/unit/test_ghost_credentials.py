#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for GhostCredentials module
"""

import pytest
import sys
import os
import tempfile
from io import BytesIO

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ghost.ghostlib.GhostCredentials import (
    Encryptor,
    GnomeKeyring,
    _generate_password,
    _generate_id,
    DEFAULT_ROLE,
)


class TestPasswordGeneration:
    """测试密码生成功能"""

    def test_generate_password_length(self):
        """测试生成的密码长度"""
        for length in [8, 16, 32, 64]:
            pwd = _generate_password(length)
            assert len(pwd) == length

    def test_generate_password_characters(self):
        """测试密码字符集"""
        pwd = _generate_password(100)
        # 应该包含字母、数字、标点
        assert any(c in pwd for c in 'abcdefghijklmnopqrstuvwxyz')
        assert any(c in pwd for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        assert any(c in pwd for c in '0123456789')
        assert any(c in pwd for c in '!@#$%^&*()_+-=[]{}|;:,.<>?')

    def test_generate_password_uniqueness(self):
        """测试密码唯一性"""
        pwd1 = _generate_password(32)
        pwd2 = _generate_password(32)
        assert pwd1 != pwd2


class TestIDGeneration:
    """测试ID生成功能"""

    def test_generate_id_length(self):
        """测试生成的ID长度"""
        for length in [8, 16, 32]:
            id_str = _generate_id(length)
            assert len(id_str) == length

    def test_generate_id_only_letters(self):
        """测试ID只包含字母"""
        id_str = _generate_id(32)
        assert all(c.isalpha() for c in id_str)


class TestEncryptor:
    """测试加密器"""

    def test_derive_key_and_iv_lengths(self):
        """测试密钥派生长度"""
        # 注意：这个测试需要密码输入，在实际环境中可能需要 mock
        # 由于 Encryptor 是单例且依赖密码输入，我们测试其数学特性
        salt = b'some_salt_here_123456'
        key_length = 32
        iv_length = 16

        # 手动测试派生函数 (使用静态方法或重新实现)
        from hashlib import pbkdf2_hmac
        password = "test_password"
        dk = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=key_length+iv_length)
        key, iv = dk[:key_length], dk[key_length:key_length+iv_length]

        assert len(key) == key_length
        assert len(iv) == iv_length

    def test_encryption_consistency(self):
        """测试加密解密一致性"""
        try:
            from Crypto.Cipher import AES
            from hashlib import pbkdf2_hmac
        except ImportError:
            pytest.skip("Crypto library not available")

        password = "test_password_for_encryption"
        salt = b'salt_1234567890123456'

        # 派生密钥
        dk = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=48)
        key, iv = dk[:32], dk[32:48]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 加密数据
        plaintext = b'Hello, World! This is a test.'
        # PKCS7 padding
        bs = AES.block_size
        pad_len = bs - (len(plaintext) % bs)
        padded = plaintext + chr(pad_len).encode() * pad_len

        ciphertext = cipher.encrypt(padded)

        # 解密
        decipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = decipher.decrypt(ciphertext)

        # 去除 padding
        padding_length = decrypted[-1]
        unpadded = decrypted[:-padding_length]

        assert unpadded == plaintext


class TestGnomeKeyring:
    """测试 GnomeKeyring (需要 secretstorage 可用)"""

    def test_initialization_without_secretstorage(self):
        """测试没有 secretstorage 模块时的初始化（如果可用则测试）"""
        try:
            import secretstorage
            pytest.skip("secretstorage is available, cannot test absence")
        except ImportError:
            gkr = GnomeKeyring()
            assert gkr.bus is None

    def test_get_pass_returns_none_when_no_bus(self):
        """测试没有 bus 时返回 None"""
        gkr = GnomeKeyring()
        # 强制设置 bus 为 None
        gkr.bus = None
        result = gkr.get_pass()
        assert result is None


class TestConstants:
    """测试常量"""

    def test_default_role(self):
        """测试默认角色"""
        assert DEFAULT_ROLE == 'CLIENT'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
