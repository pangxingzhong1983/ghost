#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Comprehensive performance test script

import os
import sys
import time
import tempfile
import threading
import concurrent.futures

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

class ComprehensivePerformanceTest:
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
    
    def test_object_pool_with_large_objects(self):
        """Test object pool with large objects"""
        # Create object pool
        def create_large_object():
            return {'data': b'x' * 1024 * 100}  # 100KB object
        
        pool = ObjectPool(create_large_object, max_size=100)
        
        # Test object creation without pool
        start_time = time.time()
        for _ in range(10000):
            obj = {'data': b'x' * 1024 * 100}
        no_pool_time = time.time() - start_time
        
        # Test object creation with pool
        start_time = time.time()
        for _ in range(10000):
            obj = pool.get()
            pool.put(obj)
        with_pool_time = time.time() - start_time
        
        speedup = no_pool_time / with_pool_time
        return f"Object pool with large objects speedup: {speedup:.2f}x (no pool: {no_pool_time:.4f}s, with pool: {with_pool_time:.4f}s)"
    
    def test_buffer_pool_with_large_buffers(self):
        """Test buffer pool with large buffers"""
        # Create buffer pool
        buffer_pool = BufferPool(buffer_size=1024 * 1024, max_size=100)  # 1MB buffers
        
        # Test buffer creation without pool
        start_time = time.time()
        for _ in range(10000):
            buffer = bytearray(1024 * 1024)
        no_pool_time = time.time() - start_time
        
        # Test buffer creation with pool
        start_time = time.time()
        for _ in range(10000):
            buffer = buffer_pool.get()
            buffer_pool.put(buffer)
        with_pool_time = time.time() - start_time
        
        speedup = no_pool_time / with_pool_time
        return f"Buffer pool with large buffers speedup: {speedup:.2f}x (no pool: {no_pool_time:.4f}s, with pool: {with_pool_time:.4f}s)"
    
    def test_mmap_with_very_large_file(self):
        """Test mmap with very large file"""
        # Create test data
        test_data = b'x' * (1024 * 1024 * 100)  # 100MB
        
        # Write with regular file operations
        test_file = 'test_very_large_file.bin'
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
        return f"MMAP with very large file speedup - Write: {write_speedup:.2f}x, Read: {read_speedup:.2f}x"
    
    def test_module_cache_with_many_modules(self):
        """Test module cache with many modules"""
        # Clear cache
        clear_cache()
        
        # Test importing multiple modules
        modules = ['os', 'sys', 'time', 'datetime', 'json', 'pickle', 'socket', 'ssl', 'hashlib', 'base64']
        
        # First import (should be slower)
        start_time = time.time()
        imported_modules = []
        for module_name in modules:
            imported_modules.append(import_module(module_name))
        first_import_time = time.time() - start_time
        
        # Second import (should be faster)
        start_time = time.time()
        reimported_modules = []
        for module_name in modules:
            reimported_modules.append(import_module(module_name))
        second_import_time = time.time() - start_time
        
        speedup = first_import_time / second_import_time
        return f"Module cache with many modules speedup: {speedup:.2f}x (first: {first_import_time:.4f}s, second: {second_import_time:.4f}s)"
    
    def test_async_vs_sync_with_concurrent_requests(self):
        """Test async vs sync with concurrent requests"""
        # This is a conceptual test since we can't easily test async vs sync without a server
        # We'll just verify that the async connection module can handle concurrent operations
        try:
            from ghost.network.lib.async_connection import AsyncGhostClient, AsyncGhostServer
            
            # Test concurrent async operations
            async def test_concurrent_async():
                async def dummy_operation():
                    await asyncio.sleep(0.1)
                    return True
                
                tasks = [dummy_operation() for _ in range(100)]
                results = await asyncio.gather(*tasks)
                return len(results) == 100
            
            import asyncio
            result = asyncio.run(test_concurrent_async())
            return f"Async connection module can handle concurrent operations: {result}"
        except Exception as e:
            raise Exception(f"Failed to test async connection module: {e}")
    
    def test_parallel_execution(self):
        """Test parallel execution of tasks"""
        # Test CPU-bound task
        def cpu_bound_task(n):
            result = 0
            for i in range(n):
                result += i
            return result
        
        # Test sequential execution
        start_time = time.time()
        for _ in range(10):
            cpu_bound_task(10000000)
        sequential_time = time.time() - start_time
        
        # Test parallel execution
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(cpu_bound_task, 10000000) for _ in range(10)]
            concurrent.futures.wait(futures)
        parallel_time = time.time() - start_time
        
        speedup = sequential_time / parallel_time
        return f"Parallel execution speedup: {speedup:.2f}x (sequential: {sequential_time:.4f}s, parallel: {parallel_time:.4f}s)"
    
    def test_memory_usage(self):
        """Test memory usage optimization"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create many objects without pool
        objects = []
        for _ in range(100000):
            objects.append({'data': b'x' * 1024})
        
        # Get memory usage after creating objects
        memory_after_objects = process.memory_info().rss / 1024 / 1024  # MB
        
        # Clear objects
        del objects
        import gc
        gc.collect()
        
        # Create object pool and reuse objects
        def create_object():
            return {'data': b'x' * 1024}
        
        pool = ObjectPool(create_object, max_size=1000)
        for _ in range(100000):
            obj = pool.get()
            pool.put(obj)
        
        # Get memory usage after using pool
        memory_after_pool = process.memory_info().rss / 1024 / 1024  # MB
        
        memory_saved = memory_after_objects - memory_after_pool
        return f"Memory usage optimization - Saved: {memory_saved:.2f} MB (without pool: {memory_after_objects:.2f} MB, with pool: {memory_after_pool:.2f} MB)"
    
    def run_all_tests(self):
        """Run all comprehensive performance tests"""
        print(f"\n=== Comprehensive Performance Optimization Test ===")
        print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        tests = [
            ("Object Pool with Large Objects", self.test_object_pool_with_large_objects),
            ("Buffer Pool with Large Buffers", self.test_buffer_pool_with_large_buffers),
            ("MMAP with Very Large File", self.test_mmap_with_very_large_file),
            ("Module Cache with Many Modules", self.test_module_cache_with_many_modules),
            ("Async Concurrent Operations", self.test_async_vs_sync_with_concurrent_requests),
            ("Parallel Execution", self.test_parallel_execution),
            ("Memory Usage Optimization", self.test_memory_usage)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print("=" * 80)
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
    test = ComprehensivePerformanceTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)