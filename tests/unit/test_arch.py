#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for architecture utility functions
"""

import pytest
import sys
import os
import platform

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ghost.ghostlib.utils.arch import (
    make_os_arch,
    make_template_arch,
    make_proc_arch,
    is_native,
    same_as_local_arch,
)


class TestMakeOsArch:
    """测试 make_os_arch 函数"""

    def test_x86_64_mapping(self):
        assert make_os_arch('x86_64') == 'amd64'

    def test_i386_mapping(self):
        assert make_os_arch('i386') == 'x86'

    def test_i686_mapping(self):
        assert make_os_arch('i686') == 'x86'

    def test_armv7l_mapping(self):
        assert make_os_arch('armv7l') == 'armhf'

    def test_arm64_mapping(self):
        assert make_os_arch('arm64') == 'arm64'

    def test_aarch64_mapping(self):
        assert make_os_arch('aarch64') == 'aarch64'  # 未映射则返回原值

    def test_unknown_arch_returns_original(self):
        assert make_os_arch('mips') == 'mips'


class TestMakeTemplateArch:
    """测试 make_template_arch 函数"""

    def test_x86_64_mapping(self):
        assert make_template_arch('x86_64') == 'x64'

    def test_amd64_mapping(self):
        assert make_template_arch('amd64') == 'x64'

    def test_i386_mapping(self):
        assert make_template_arch('i386') == 'x86'

    def test_armv7l_mapping(self):
        assert make_template_arch('armv7l') == 'armhf'

    def test_arm64_mapping(self):
        assert make_template_arch('arm64') == 'arm64'


class TestMakeProcArch:
    """测试 make_proc_arch 函数"""

    def test_amd64_64bit(self):
        assert make_proc_arch('amd64', '64bit') == 'amd64'

    def test_amd64_32bit(self):
        assert make_proc_arch('amd64', '32bit') == 'x86'

    def test_arm64_64bit(self):
        assert make_proc_arch('arm64', '64bit') == 'aarch64'

    def test_armhf_64bit(self):
        assert make_proc_arch('armhf', '64bit') == 'armhf'

    def test_armhf_32bit(self):
        assert make_proc_arch('armhf', '32bit') == 'armhf'

    def test_unknown_arch_returns_proc(self):
        # 未知架构应原样返回 proc_arch
        assert make_proc_arch('mips', '64bit') == '64bit'


class TestIsNative:
    """测试 is_native 函数"""

    def test_is_native_logic(self):
        """测试 is_native 的逻辑"""
        # 测试已知架构组合
        result = is_native('Linux', 'x86_64', '3.10')
        # 仅在本地匹配时为 True，这里只是测试不崩溃
        assert isinstance(result, bool)


class TestSameAsLocalArch:
    """测试 same_as_local_arch 函数"""

    def test_same_as_local_arch_logic(self):
        """测试 same_as_local_arch 的逻辑"""
        result = same_as_local_arch('linux', 'amd64')
        assert isinstance(result, bool)


if __name__ == '__main__':
    import platform
    pytest.main([__file__, '-v'])
