#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import threading
import queue
import time

class ObjectPool:
    def __init__(self, create_func, max_size=100, max_idle_time=300):
        """
        创建对象池
        
        Args:
            create_func: 创建对象的函数
            max_size: 池的最大大小
            max_idle_time: 对象最大空闲时间（秒）
        """
        self.create_func = create_func
        self.max_size = max_size
        self.max_idle_time = max_idle_time
        self.pool = queue.Queue(maxsize=max_size)
        self.lock = threading.RLock()
        self.size = 0
        self.last_used = {}
        
        # 启动清理线程
        self.cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        self.cleanup_thread.start()
    
    def _cleanup(self):
        """定期清理过期的对象"""
        while True:
            time.sleep(60)  # 每分钟检查一次
            with self.lock:
                current_time = time.time()
                expired_ids = []
                
                # 检查所有对象的空闲时间
                for obj_id, last_time in list(self.last_used.items()):
                    if current_time - last_time > self.max_idle_time:
                        expired_ids.append(obj_id)
                
                # 从池中移除过期对象
                for obj_id in expired_ids:
                    try:
                        # 尝试从队列中移除对象
                        # 注意：这不是最高效的方法，但对于小池来说足够了
                        temp_queue = queue.Queue(maxsize=self.max_size)
                        while not self.pool.empty():
                            item = self.pool.get()
                            if id(item) != obj_id:
                                temp_queue.put(item)
                            else:
                                self.size -= 1
                                if obj_id in self.last_used:
                                    del self.last_used[obj_id]
                        # 将剩余对象放回池中
                        while not temp_queue.empty():
                            self.pool.put(temp_queue.get())
                    except Exception as e:
                        pass
    
    def get(self, timeout=None):
        """
        从池中获取对象
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            对象实例
        """
        try:
            # 尝试从池中获取对象
            obj = self.pool.get(block=timeout is not None, timeout=timeout)
            with self.lock:
                self.last_used[id(obj)] = time.time()
            return obj
        except queue.Empty:
            # 池中没有对象，创建新对象
            with self.lock:
                if self.size < self.max_size:
                    obj = self.create_func()
                    self.size += 1
                    self.last_used[id(obj)] = time.time()
                    return obj
                else:
                    # 池已满，等待
                    obj = self.pool.get()
                    self.last_used[id(obj)] = time.time()
                    return obj
    
    def put(self, obj):
        """
        将对象放回池中
        
        Args:
            obj: 要放回池中的对象
        """
        try:
            self.pool.put(obj, block=False)
            with self.lock:
                self.last_used[id(obj)] = time.time()
        except queue.Full:
            # 池已满，丢弃对象
            with self.lock:
                obj_id = id(obj)
                if obj_id in self.last_used:
                    del self.last_used[obj_id]
                self.size -= 1
    
    def clear(self):
        """清空池"""
        with self.lock:
            while not self.pool.empty():
                try:
                    obj = self.pool.get(block=False)
                    obj_id = id(obj)
                    if obj_id in self.last_used:
                        del self.last_used[obj_id]
                except queue.Empty:
                    break
            self.size = 0
            self.last_used.clear()
    
    def get_size(self):
        """
        获取当前池的大小
        
        Returns:
            池中的对象数量
        """
        return self.size
    
    def get_max_size(self):
        """
        获取池的最大大小
        
        Returns:
            池的最大大小
        """
        return self.max_size

class BufferPool(ObjectPool):
    def __init__(self, buffer_size=4096, max_size=100):
        """
        创建缓冲区池
        
        Args:
            buffer_size: 缓冲区大小
            max_size: 池的最大大小
        """
        def create_buffer():
            return bytearray(buffer_size)
        
        super().__init__(create_buffer, max_size=max_size)
        self.buffer_size = buffer_size
    
    def get(self, timeout=None):
        """
        从池中获取缓冲区
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            缓冲区
        """
        buffer = super().get(timeout)
        # 重置缓冲区
        buffer[:] = b'\x00' * self.buffer_size
        return buffer

class ConnectionPool(ObjectPool):
    def __init__(self, create_func, max_size=10):
        """
        创建连接池
        
        Args:
            create_func: 创建连接的函数
            max_size: 池的最大大小
        """
        super().__init__(create_func, max_size=max_size)
    
    def get(self, timeout=None):
        """
        从池中获取连接
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            连接对象
        """
        connection = super().get(timeout)
        # 检查连接是否有效
        if hasattr(connection, 'is_connected') and not connection.is_connected():
            # 连接已断开，创建新连接
            with self.lock:
                self.size -= 1
                if connection in self.last_used:
                    del self.last_used[connection]
            return self.create_func()
        return connection
    
    def put(self, connection):
        """
        将连接放回池中
        
        Args:
            connection: 要放回池中的连接
        """
        # 检查连接是否有效
        if hasattr(connection, 'is_connected') and not connection.is_connected():
            # 连接已断开，不放入池中
            with self.lock:
                connection_id = id(connection)
                if connection_id in self.last_used:
                    del self.last_used[connection_id]
                self.size -= 1
        else:
            super().put(connection)

if __name__ == '__main__':
    # 测试对象池
    def create_test_object():
        return {}
    
    pool = ObjectPool(create_test_object, max_size=5)
    
    # 获取对象
    objs = []
    for i in range(10):
        obj = pool.get()
        obj['id'] = i
        objs.append(obj)
        print(f"Got object {i}: {obj}")
    
    # 放回对象
    for i, obj in enumerate(objs):
        pool.put(obj)
        print(f"Put back object {i}: {obj}")
    
    # 再次获取对象
    for i in range(5):
        obj = pool.get()
        print(f"Got object again {i}: {obj}")
        pool.put(obj)
    
    print(f"Pool size: {pool.get_size()}")
    
    # 测试缓冲区池
    buffer_pool = BufferPool(buffer_size=1024, max_size=3)
    
    # 获取缓冲区
    buffers = []
    for i in range(5):
        buffer = buffer_pool.get()
        buffer[:10] = b'Hello ' + str(i).encode()
        buffers.append(buffer)
        print(f"Got buffer {i}: {buffer[:20]}")
    
    # 放回缓冲区
    for i, buffer in enumerate(buffers):
        buffer_pool.put(buffer)
        print(f"Put back buffer {i}")
    
    # 再次获取缓冲区
    for i in range(3):
        buffer = buffer_pool.get()
        print(f"Got buffer again {i}: {buffer[:20]}")
        buffer_pool.put(buffer)
    
    print(f"Buffer pool size: {buffer_pool.get_size()}")