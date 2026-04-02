#!/usr/bin/env python3
"""
Performance test script for Ghost
"""

import time
import memory_profiler
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_memory_usage():
    """Test memory usage of core modules"""
    print("Testing memory usage...")
    
    # Import core modules
    from ghost.ghostlib import GhostClient, GhostServer
    from ghost.network.lib.transports import http
    
    # Measure memory after imports
    mem_usage = memory_profiler.memory_usage()[0]
    print(f"Memory usage after imports: {mem_usage:.2f} MB")
    
    return mem_usage

def test_execution_speed():
    """Test execution speed of common operations"""
    print("\nTesting execution speed...")
    
    # Test encryption speed
    from ghost.network.lib.transports.cryptoutils.aes import NewAESCipher, AES_MODE_GCM
    import os
    
    # Generate test data
    test_data = os.urandom(1024 * 1024)  # 1MB of random data
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)   # 128-bit IV
    
    # Test encryption
    start_time = time.time()
    cipher = NewAESCipher(key, iv, mode=AES_MODE_GCM)
    encrypted, tag = cipher.encrypt_and_digest(test_data)
    encryption_time = time.time() - start_time
    print(f"Encryption speed: {len(test_data) / (encryption_time * 1024 * 1024):.2f} MB/s")
    
    # Test decryption
    start_time = time.time()
    cipher = NewAESCipher(key, iv, mode=AES_MODE_GCM)
    decrypted = cipher.decrypt_and_verify(encrypted, tag)
    decryption_time = time.time() - start_time
    print(f"Decryption speed: {len(test_data) / (decryption_time * 1024 * 1024):.2f} MB/s")
    
    return encryption_time, decryption_time

def test_module_loading():
    """Test module loading time"""
    print("\nTesting module loading time...")
    
    modules = [
        "ghost.ghostlib",
        "ghost.network.lib",
        "ghost.modules",
        "ghost.packages"
    ]
    
    for module in modules:
        start_time = time.time()
        __import__(module)
        load_time = time.time() - start_time
        print(f"Loading {module}: {load_time:.4f} seconds")

def main():
    """Run all performance tests"""
    print("=== Ghost Performance Test ===")
    
    test_memory_usage()
    test_execution_speed()
    test_module_loading()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()