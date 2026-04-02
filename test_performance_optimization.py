#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Test script for performance optimization

import os
import sys
import time
import tempfile
import threading

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghost.ghostlib.utils.object_pool import ObjectPool, BufferPool, ConnectionPool
from ghost.ghostlib.utils.mmap_handler import MmapHandler, MmapBuffer
from ghost.ghostlib.utils.module_cache import import_module, get_cache_stats, clear_cache
from ghost.ghostlib.utils.antivirus_evasion import AntivirusEvasion
from ghost.ghostlib.GhostConfig import GhostConfig

class TestResult:
    def __init__(self, test_name, passed, message, duration=None):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.duration = duration

class PerformanceTest:
    def __init__(self):
        self.config = GhostConfig()
        self.results = []
    
    def run_test(self, test_name, test_func):
        """Run a test and record the result"""
        start_time = time.time()
        try:
            result = test_func()
            duration = time.time() - start_time
            self.results.append(TestResult(test_name, True, result, duration))
            print(f"✅ {test_name}: PASSED - {result} (took {duration:.4f}s)")
        except Exception as e:
            duration = time.time() - start_time
            self.results.append(TestResult(test_name, False, str(e), duration))
            print(f"❌ {test_name}: FAILED - {str(e)} (took {duration:.4f}s)")
    
    def test_object_pool(self):
        """Test object pool performance"""
        # Create object pool
        def create_test_object():
            return {}
        
        pool = ObjectPool(create_test_object, max_size=100)
        
        # Test object creation without pool
        start_time = time.time()
        for _ in range(10000):
            obj = {}
        no_pool_time = time.time() - start_time
        
        # Test object creation with pool
        start_time = time.time()
        for _ in range(10000):
            obj = pool.get()
            pool.put(obj)
        with_pool_time = time.time() - start_time
        
        speedup = no_pool_time / with_pool_time
        return f"Object pool speedup: {speedup:.2f}x (no pool: {no_pool_time:.4f}s, with pool: {with_pool_time:.4f}s)"
    
    def test_buffer_pool(self):
        """Test buffer pool performance"""
        # Create buffer pool
        buffer_pool = BufferPool(buffer_size=4096, max_size=100)
        
        # Test buffer creation without pool
        start_time = time.time()
        for _ in range(10000):
            buffer = bytearray(4096)
        no_pool_time = time.time() - start_time
        
        # Test buffer creation with pool
        start_time = time.time()
        for _ in range(10000):
            buffer = buffer_pool.get()
            buffer_pool.put(buffer)
        with_pool_time = time.time() - start_time
        
        speedup = no_pool_time / with_pool_time
        return f"Buffer pool speedup: {speedup:.2f}x (no pool: {no_pool_time:.4f}s, with pool: {with_pool_time:.4f}s)"
    
    def test_mmap_large_file(self):
        """Test mmap for large file operations"""
        # Create test data
        test_data = b'x' * (1024 * 1024 * 10)  # 10MB
        
        # Write with regular file operations
        test_file = 'test_large_file.bin'
        start_time = time.time()
        with open(test_file, 'wb') as f:
            f.write(test_data)
        regular_write_time = time.time() - start_time
        
        # Read with regular file operations
        start_time = time.time()
        with open(test_file, 'rb') as f:
            data = f.read()
        regular_read_time = time.time() - start_time
        
        # Write with mmap
        start_time = time.time()
        MmapHandler.write_large_file(test_file + '.mmap', test_data)
        mmap_write_time = time.time() - start_time
        
        # Read with mmap
        start_time = time.time()
        chunks = []
        for chunk in MmapHandler.read_large_file(test_file + '.mmap'):
            chunks.append(chunk)
        mmap_read_time = time.time() - start_time
        
        # Clean up
        os.unlink(test_file)
        os.unlink(test_file + '.mmap')
        
        write_speedup = regular_write_time / mmap_write_time
        read_speedup = regular_read_time / mmap_read_time
        return f"MMAP speedup - Write: {write_speedup:.2f}x, Read: {read_speedup:.2f}x"
    
    def test_module_cache(self):
        """Test module cache performance"""
        # Clear cache
        clear_cache()
        
        # First import (should be slower)
        start_time = time.time()
        module1 = import_module('os')
        first_import_time = time.time() - start_time
        
        # Second import (should be faster)
        start_time = time.time()
        module2 = import_module('os')
        second_import_time = time.time() - start_time
        
        speedup = first_import_time / second_import_time
        return f"Module cache speedup: {speedup:.2f}x (first: {first_import_time:.4f}s, second: {second_import_time:.4f}s)"
    
    def test_async_vs_sync(self):
        """Test async vs sync performance"""
        # This is a conceptual test since we can't easily test async vs sync without a server
        # We'll just verify that the async connection module loads correctly
        try:
            from ghost.network.lib.async_connection import AsyncGhostClient, AsyncGhostServer
            return "Async connection module loaded successfully"
        except Exception as e:
            raise Exception(f"Failed to load async connection module: {e}")
    
    def run_all_tests(self):
        """Run all performance tests"""
        print(f"\n=== Performance Optimization Test ===")
        print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ("Object Pool Performance", self.test_object_pool),
            ("Buffer Pool Performance", self.test_buffer_pool),
            ("MMAP Large File Operations", self.test_mmap_large_file),
            ("Module Cache Performance", self.test_module_cache),
            ("Async Connection Module", self.test_async_vs_sync)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print("=" * 60)
        print("\n=== Test Summary ===")
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        print(f"Passed: {passed}/{total}")
        
        if passed == total:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed:")
            for result in self.results:
                if not result.passed:
                    print(f"  - {result.test_name}: {result.message}")
        
        # Print performance summary
        print("\n=== Performance Summary ===")
        for result in self.results:
            if result.passed and result.duration:
                print(f"{result.test_name}: {result.message}")
        
        return passed == total

if __name__ == "__main__":
    test = PerformanceTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)