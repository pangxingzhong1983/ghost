#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import mmap
import os
import tempfile
import contextlib

class MmapHandler:
    """
    内存映射处理类，用于高效处理大型数据
    """
    
    @staticmethod
    def create_mmap(file_path, size=None, access=mmap.ACCESS_DEFAULT):
        """
        创建内存映射
        
        Args:
            file_path: 文件路径
            size: 映射大小，如果为None则使用文件大小
            access: 访问模式
            
        Returns:
            mmap对象
        """
        with open(file_path, 'r+b') as f:
            if size is None:
                size = os.path.getsize(file_path)
            return mmap.mmap(f.fileno(), size, access=access)
    
    @staticmethod
    def create_temp_mmap(data=None, size=1024*1024):
        """
        创建临时文件的内存映射
        
        Args:
            data: 初始数据
            size: 映射大小
            
        Returns:
            (mmap对象, 临时文件路径)
        """
        fd, temp_path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w+b') as f:
                if data:
                    f.write(data)
                f.truncate(size)
            
            mm = MmapHandler.create_mmap(temp_path, size)
            return mm, temp_path
        except Exception as e:
            os.close(fd)
            os.unlink(temp_path)
            raise e
    
    @staticmethod
    @contextlib.contextmanager
    def temp_mmap(data=None, size=1024*1024):
        """
        临时内存映射上下文管理器
        
        Args:
            data: 初始数据
            size: 映射大小
            
        Yields:
            mmap对象
        """
        mm, temp_path = None, None
        try:
            mm, temp_path = MmapHandler.create_temp_mmap(data, size)
            yield mm
        finally:
            if mm:
                mm.close()
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
    
    @staticmethod
    def read_large_file(file_path, chunk_size=1024*1024):
        """
        使用内存映射读取大型文件
        
        Args:
            file_path: 文件路径
            chunk_size: 块大小
            
        Yields:
            数据块
        """
        with open(file_path, 'r+b') as f:
            size = os.path.getsize(file_path)
            with mmap.mmap(f.fileno(), size) as mm:
                for i in range(0, size, chunk_size):
                    yield mm[i:i+chunk_size]
    
    @staticmethod
    def write_large_file(file_path, data):
        """
        使用内存映射写入大型文件
        
        Args:
            file_path: 文件路径
            data: 数据
        """
        with open(file_path, 'w+b') as f:
            f.write(data)
            f.flush()
            size = len(data)
            with mmap.mmap(f.fileno(), size) as mm:
                mm[:size] = data
                mm.flush()
    
    @staticmethod
    def copy_large_file(src_path, dst_path):
        """
        使用内存映射复制大型文件
        
        Args:
            src_path: 源文件路径
            dst_path: 目标文件路径
        """
        src_size = os.path.getsize(src_path)
        
        # 创建目标文件
        with open(dst_path, 'w+b') as dst_f:
            dst_f.truncate(src_size)
            
            # 映射源文件和目标文件
            with open(src_path, 'r+b') as src_f:
                with mmap.mmap(src_f.fileno(), src_size) as src_mm:
                    with mmap.mmap(dst_f.fileno(), src_size) as dst_mm:
                        # 复制数据
                        dst_mm[:] = src_mm[:]
                        dst_mm.flush()
    
    @staticmethod
    def search_in_file(file_path, pattern):
        """
        使用内存映射在文件中搜索模式
        
        Args:
            file_path: 文件路径
            pattern: 搜索模式（字节串）
            
        Returns:
            匹配的位置列表
        """
        positions = []
        pattern_len = len(pattern)
        
        with open(file_path, 'r+b') as f:
            size = os.path.getsize(file_path)
            with mmap.mmap(f.fileno(), size) as mm:
                pos = 0
                while pos < size:
                    pos = mm.find(pattern, pos)
                    if pos == -1:
                        break
                    positions.append(pos)
                    pos += pattern_len
        
        return positions

class MmapBuffer:
    """
    基于内存映射的缓冲区
    """
    
    def __init__(self, size=1024*1024):
        """
        初始化内存映射缓冲区
        
        Args:
            size: 缓冲区大小
        """
        self.size = size
        self.mm, self.temp_path = MmapHandler.create_temp_mmap(size=size)
        self.position = 0
    
    def write(self, data):
        """
        写入数据
        
        Args:
            data: 要写入的数据
            
        Returns:
            写入的字节数
        """
        data_len = len(data)
        if self.position + data_len > self.size:
            # 扩展缓冲区
            new_size = max(self.size * 2, self.position + data_len)
            self._resize(new_size)
        
        self.mm[self.position:self.position+data_len] = data
        self.position += data_len
        return data_len
    
    def read(self, size=-1):
        """
        读取数据
        
        Args:
            size: 读取的字节数，-1表示读取所有数据
            
        Returns:
            读取的数据
        """
        if size == -1:
            size = self.position
        
        end_pos = min(self.position, self.position + size)
        data = self.mm[self.position:end_pos]
        self.position = end_pos
        return data
    
    def seek(self, offset, whence=0):
        """
        设置文件指针位置
        
        Args:
            offset: 偏移量
            whence: 基准位置，0表示文件开头，1表示当前位置，2表示文件末尾
        """
        if whence == 0:
            self.position = offset
        elif whence == 1:
            self.position += offset
        elif whence == 2:
            self.position = self.size + offset
        
        # 确保位置在有效范围内
        self.position = max(0, min(self.position, self.size))
    
    def tell(self):
        """
        获取当前文件指针位置
        
        Returns:
            当前位置
        """
        return self.position
    
    def flush(self):
        """
        刷新缓冲区
        """
        self.mm.flush()
    
    def _resize(self, new_size):
        """
        调整缓冲区大小
        
        Args:
            new_size: 新的大小
        """
        # 创建新的临时文件和内存映射
        new_mm, new_temp_path = MmapHandler.create_temp_mmap(size=new_size)
        
        # 复制数据
        data_len = min(self.size, new_size)
        new_mm[:data_len] = self.mm[:data_len]
        new_mm.flush()
        
        # 清理旧的映射和文件
        self.mm.close()
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
        
        # 更新属性
        self.mm = new_mm
        self.temp_path = new_temp_path
        self.size = new_size
    
    def close(self):
        """
        关闭缓冲区
        """
        if self.mm:
            self.mm.close()
            self.mm = None
        if self.temp_path and os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
            self.temp_path = None
    
    def __del__(self):
        """
        析构函数
        """
        self.close()
    
    def __enter__(self):
        """
        进入上下文管理器
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器
        """
        self.close()

if __name__ == '__main__':
    # 测试内存映射处理
    test_data = b'Hello, memory mapped world!' * 1000
    
    # 测试临时内存映射
    print("Testing temp mmap...")
    with MmapHandler.temp_mmap(test_data) as mm:
        print(f"Mmap size: {mm.size()}")
        print(f"First 50 bytes: {mm[:50]}")
        
        # 修改数据
        mm[0:5] = b'Hi, '
        print(f"Modified first 50 bytes: {mm[:50]}")
    
    # 测试读写大型文件
    print("\nTesting large file operations...")
    test_file = 'test_large_file.bin'
    
    # 写入大型文件
    MmapHandler.write_large_file(test_file, test_data)
    print(f"Written test file: {test_file}")
    
    # 读取大型文件
    chunks = []
    for chunk in MmapHandler.read_large_file(test_file, chunk_size=100):
        chunks.append(chunk)
    read_data = b''.join(chunks)
    print(f"Read {len(read_data)} bytes from test file")
    print(f"Data matches: {read_data == test_data}")
    
    # 搜索文件
    print("\nTesting search in file...")
    pattern = b'world'
    positions = MmapHandler.search_in_file(test_file, pattern)
    print(f"Found pattern '{pattern}' at positions: {positions}")
    
    # 复制文件
    print("\nTesting file copy...")
    copy_file = 'test_copy.bin'
    MmapHandler.copy_large_file(test_file, copy_file)
    
    # 验证复制
    with open(test_file, 'rb') as f1, open(copy_file, 'rb') as f2:
        print(f"Files are identical: {f1.read() == f2.read()}")
    
    # 清理测试文件
    os.unlink(test_file)
    os.unlink(copy_file)
    
    # 测试内存映射缓冲区
    print("\nTesting MmapBuffer...")
    with MmapBuffer(size=100) as buf:
        # 写入数据
        buf.write(b'Hello, ')
        buf.write(b'world!')
        print(f"Buffer position after write: {buf.tell()}")
        
        # 重置位置
        buf.seek(0)
        
        # 读取数据
        data = buf.read()
        print(f"Read from buffer: {data}")
        
        # 测试扩展缓冲区
        large_data = b'x' * 200
        buf.seek(0)
        written = buf.write(large_data)
        print(f"Wrote {written} bytes to buffer")
        print(f"Buffer size after expansion: {buf.size}")
    
    print("\nAll tests completed!")