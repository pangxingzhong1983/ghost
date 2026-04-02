#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import importlib
import importlib.util
import sys
import os
import hashlib
import threading
import time

class ModuleCache:
    """
    模块缓存系统，用于优化模块加载速度
    """
    
    def __init__(self, max_size=100, max_age=3600):
        """
        初始化模块缓存
        
        Args:
            max_size: 缓存的最大模块数量
            max_age: 模块的最大缓存时间（秒）
        """
        self.max_size = max_size
        self.max_age = max_age
        self.cache = {}
        self.lock = threading.RLock()
        self.access_times = {}
        
        # 启动清理线程
        self.cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        self.cleanup_thread.start()
    
    def _cleanup(self):
        """定期清理过期的模块"""
        while True:
            time.sleep(60)  # 每分钟检查一次
            current_time = time.time()
            
            with self.lock:
                expired = []
                for module_name, timestamp in list(self.access_times.items()):
                    if current_time - timestamp > self.max_age:
                        expired.append(module_name)
                
                # 清理过期模块
                for module_name in expired:
                    if module_name in self.cache:
                        del self.cache[module_name]
                    if module_name in self.access_times:
                        del self.access_times[module_name]
                
                # 如果缓存超过最大大小，清理最旧的模块
                if len(self.cache) > self.max_size:
                    # 按访问时间排序
                    sorted_modules = sorted(
                        self.access_times.items(),
                        key=lambda x: x[1]
                    )
                    # 删除最旧的模块
                    to_remove = len(self.cache) - self.max_size
                    for module_name, _ in sorted_modules[:to_remove]:
                        if module_name in self.cache:
                            del self.cache[module_name]
                        if module_name in self.access_times:
                            del self.access_times[module_name]
    
    def get_module(self, module_name):
        """
        从缓存中获取模块
        
        Args:
            module_name: 模块名称
            
        Returns:
            模块对象
        """
        with self.lock:
            if module_name in self.cache:
                # 更新访问时间
                self.access_times[module_name] = time.time()
                return self.cache[module_name]
            return None
    
    def add_module(self, module_name, module):
        """
        将模块添加到缓存
        
        Args:
            module_name: 模块名称
            module: 模块对象
        """
        with self.lock:
            # 如果缓存超过最大大小，删除最旧的模块
            if len(self.cache) >= self.max_size:
                # 按访问时间排序
                sorted_modules = sorted(
                    self.access_times.items(),
                    key=lambda x: x[1]
                )
                # 删除最旧的模块
                oldest_module = sorted_modules[0][0]
                if oldest_module in self.cache:
                    del self.cache[oldest_module]
                if oldest_module in self.access_times:
                    del self.access_times[oldest_module]
            
            # 添加新模块
            self.cache[module_name] = module
            self.access_times[module_name] = time.time()
    
    def remove_module(self, module_name):
        """
        从缓存中移除模块
        
        Args:
            module_name: 模块名称
        """
        with self.lock:
            if module_name in self.cache:
                del self.cache[module_name]
            if module_name in self.access_times:
                del self.access_times[module_name]
    
    def clear(self):
        """
        清空缓存
        """
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def get_size(self):
        """
        获取缓存大小
        
        Returns:
            缓存中的模块数量
        """
        with self.lock:
            return len(self.cache)
    
    def get_stats(self):
        """
        获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        with self.lock:
            current_time = time.time()
            ages = []
            for module_name, timestamp in self.access_times.items():
                ages.append(current_time - timestamp)
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'average_age': sum(ages) / len(ages) if ages else 0,
                'oldest_age': max(ages) if ages else 0,
                'youngest_age': min(ages) if ages else 0
            }

class CachedImporter:
    """
    缓存导入器，用于优化模块导入速度
    """
    
    def __init__(self, module_cache=None):
        """
        初始化缓存导入器
        
        Args:
            module_cache: 模块缓存对象，如果为None则创建默认缓存
        """
        self.module_cache = module_cache or ModuleCache()
    
    def import_module(self, module_name):
        """
        导入模块，优先从缓存中获取
        
        Args:
            module_name: 模块名称
            
        Returns:
            模块对象
        """
        # 先从缓存中获取
        module = self.module_cache.get_module(module_name)
        if module:
            return module
        
        # 缓存中没有，使用标准导入
        try:
            module = importlib.import_module(module_name)
            # 添加到缓存
            self.module_cache.add_module(module_name, module)
            return module
        except ImportError:
            raise
    
    def import_from_path(self, module_name, file_path):
        """
        从路径导入模块
        
        Args:
            module_name: 模块名称
            file_path: 文件路径
            
        Returns:
            模块对象
        """
        # 生成缓存键
        cache_key = f"{module_name}:{file_path}"
        
        # 先从缓存中获取
        module = self.module_cache.get_module(cache_key)
        if module:
            return module
        
        # 缓存中没有，从路径导入
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                # 添加到缓存
                self.module_cache.add_module(cache_key, module)
                return module
            else:
                raise ImportError(f"Could not load module from {file_path}")
        except Exception as e:
            raise ImportError(f"Error importing module from {file_path}: {e}")
    
    def get_cache_stats(self):
        """
        获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        return self.module_cache.get_stats()

# 全局模块缓存实例
global_module_cache = ModuleCache()
global_cached_importer = CachedImporter(global_module_cache)

# 替换标准导入函数
def cached_import(module_name, *args, **kwargs):
    """
    缓存版本的importlib.import_module
    """
    return global_cached_importer.import_module(module_name)

# 便捷函数
def import_module(module_name):
    """
    从缓存导入模块
    """
    return cached_import(module_name)

def import_from_path(module_name, file_path):
    """
    从路径导入模块并缓存
    """
    return global_cached_importer.import_from_path(module_name, file_path)

def get_cache_stats():
    """
    获取全局缓存统计信息
    """
    return global_module_cache.get_stats()

def clear_cache():
    """
    清空全局缓存
    """
    global_module_cache.clear()

if __name__ == '__main__':
    # 测试模块缓存
    print("Testing module cache...")
    
    # 导入模块
    import time
    
    # 第一次导入（应该较慢）
    start_time = time.time()
    module1 = import_module('os')
    first_import_time = time.time() - start_time
    print(f"First import time: {first_import_time:.4f} seconds")
    
    # 第二次导入（应该较快）
    start_time = time.time()
    module2 = import_module('os')
    second_import_time = time.time() - start_time
    print(f"Second import time: {second_import_time:.4f} seconds")
    
    # 验证是否是同一个模块
    print(f"Same module: {module1 is module2}")
    
    # 导入另一个模块
    module3 = import_module('sys')
    print(f"Imported sys module: {module3}")
    
    # 获取缓存统计信息
    stats = get_cache_stats()
    print(f"Cache stats: {stats}")
    
    # 测试从路径导入
    print("\nTesting import from path...")
    import tempfile
    
    # 创建临时模块文件
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        f.write(b'\ndef test_function():\n    return "Hello from test module"\n')
        temp_module_path = f.name
    
    try:
        # 导入临时模块
        temp_module = import_from_path('temp_module', temp_module_path)
        print(f"Imported temp module: {temp_module}")
        print(f"Test function result: {temp_module.test_function()}")
        
        # 再次导入
        temp_module2 = import_from_path('temp_module', temp_module_path)
        print(f"Same temp module: {temp_module is temp_module2}")
    finally:
        # 清理临时文件
        import os
        os.unlink(temp_module_path)
    
    # 清空缓存
    clear_cache()
    print(f"Cache size after clear: {get_cache_stats()['size']}")
    
    print("\nAll tests completed!")