#!/usr/bin/env python3
# -*- coding: UTF8 -*-
"""
测试套件，用于验证Ghost项目的功能和代码质量
"""

import os
import sys
import unittest
import importlib

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

class TestModuleImport(unittest.TestCase):
    """测试模块导入"""
    
    def test_browser_module_import(self):
        """测试browser模块导入"""
        try:
            import ghost.modules.browser
            print("✅ browser模块导入成功")
        except ImportError as e:
            self.fail(f"browser模块导入失败: {e}")
    
    def test_persistence_module_import(self):
        """测试persistence模块导入"""
        try:
            import ghost.modules.persistence
            print("✅ persistence模块导入成功")
        except ImportError as e:
            self.fail(f"persistence模块导入失败: {e}")
    
    def test_credcap_module_import(self):
        """测试credcap模块导入"""
        try:
            import ghost.modules.credcap
            print("✅ credcap模块导入成功")
        except ImportError as e:
            self.fail(f"credcap模块导入失败: {e}")
    
    def test_port_scan_module_import(self):
        """测试port_scan模块导入"""
        try:
            import ghost.modules.port_scan
            print("✅ port_scan模块导入成功")
        except ImportError as e:
            self.fail(f"port_scan模块导入失败: {e}")

class TestM2CryptoFallback(unittest.TestCase):
    """测试M2Crypto缺失时的回退机制"""
    
    def test_ghost_credentials_import(self):
        """测试GhostCredentials导入"""
        try:
            import ghost.ghostlib.GhostCredentials
            print("✅ GhostCredentials导入成功")
        except ImportError as e:
            self.fail(f"GhostCredentials导入失败: {e}")
    
    def test_jarsigner_import(self):
        """测试jarsigner导入"""
        try:
            import ghost.ghostlib.utils.jarsigner
            print("✅ jarsigner导入成功")
        except ImportError as e:
            self.fail(f"jarsigner导入失败: {e}")
    
    def test_x509_import(self):
        """测试x509导入"""
        try:
            import ghost.modules.x509
            print("✅ x509模块导入成功")
        except ImportError as e:
            self.fail(f"x509模块导入失败: {e}")

class TestPython3Compatibility(unittest.TestCase):
    """测试Python 3兼容性"""
    
    def test_mimipy_python3_compatibility(self):
        """测试mimipy.py的Python 3兼容性"""
        try:
            with open('ghost/packages/linux/all/mimipy.py', 'r') as f:
                content = f.read()
            # 检查是否有Python 2的print语句（使用正则表达式）
            import re
            # 匹配Python 2的print语句，如 print "hello" 或 print ("hello")
            python2_print_pattern = re.compile(r'^\s*print\s+(?![(])', re.MULTILINE)
            matches = python2_print_pattern.findall(content)
            self.assertEqual(len(matches), 0, "mimipy.py中存在Python 2的print语句")
            print("✅ mimipy.py Python 3兼容性检查通过")
        except Exception as e:
            self.fail(f"mimipy.py兼容性检查失败: {e}")

if __name__ == '__main__':
    print("=== Ghost 项目测试套件 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 运行测试
    unittest.main()