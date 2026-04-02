#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import asyncio
import sys
import weakref
import traceback
import zlib

from ghost.network.lib import getLogger
from ghost.network.lib.ack import Ack
from ghost.network.lib.buffer import Buffer
from ghost.network.lib.rpc.core import Connection, consts, brine, netref
from ghost.network.lib.rpc.core.consts import (
    HANDLE_PING, HANDLE_CLOSE, HANDLE_GETROOT,
    HANDLE_DIR, HANDLE_HASH, HANDLE_DEL
)

logger = getLogger('async_conn')

FAST_CALLS = (
    HANDLE_PING, HANDLE_CLOSE, HANDLE_GETROOT,
    HANDLE_DIR, HANDLE_HASH, HANDLE_DEL
)

PY2TO3_CALLATTRS = (
    '__getitem__', '__delitem__', '__setitem__',
    '__getattr__', '__delattr__', '__setattr__',
    '__getattribute__'
)

CONTROL_NOP = 0
CONTROL_ENABLE_BRINE_EXT_V1 = 1

BRINE_VER_1 = 1
PING_V1_CONTROL_MAGIC = b'\x00CTRL\x00V1'

def stream_dump(obj, version=0):
    buf = Buffer()
    brine._dump(obj, buf, version)
    return buf

class AsyncGhostConnection:
    def __init__(self, reader, writer, timeout=30):
        self.reader = reader
        self.writer = writer
        self.timeout = timeout
        self.closed = False
        self.lock = asyncio.Lock()
        self.buffer = b''
    
    async def read(self, size):
        """Async read with timeout"""
        try:
            data = await asyncio.wait_for(
                self.reader.read(size),
                timeout=self.timeout
            )
            if not data:
                self.closed = True
                raise ConnectionError("Connection closed")
            return data
        except asyncio.TimeoutError:
            self.closed = True
            raise TimeoutError("Read timeout")
    
    async def readexactly(self, size):
        """Async readexactly with timeout"""
        try:
            data = await asyncio.wait_for(
                self.reader.readexactly(size),
                timeout=self.timeout
            )
            return data
        except asyncio.TimeoutError:
            self.closed = True
            raise TimeoutError("Read timeout")
        except asyncio.IncompleteReadError:
            self.closed = True
            raise ConnectionError("Connection closed")
    
    async def write(self, data):
        """Async write with timeout"""
        try:
            async with self.lock:
                self.writer.write(data)
                await asyncio.wait_for(
                    self.writer.drain(),
                    timeout=self.timeout
                )
        except asyncio.TimeoutError:
            self.closed = True
            raise TimeoutError("Write timeout")
    
    async def close(self):
        """Close the connection"""
        if not self.closed:
            self.closed = True
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception as e:
                logger.debug(f"Error closing connection: {e}")
    
    async def recv(self):
        """Receive data with compression support"""
        # Read header
        header = await self.readexactly(4)
        size = int.from_bytes(header, byteorder='big')
        
        # Read payload
        payload = await self.readexactly(size)
        
        # Check if compressed
        if payload.startswith(b'\x78\xda'):  # zlib magic number
            try:
                payload = zlib.decompress(payload)
            except zlib.error:
                logger.warning("Failed to decompress payload, using as-is")
        
        return payload
    
    async def send(self, data):
        """Send data with compression support"""
        # Compress data if it's large enough
        if len(data) > 1024:
            compressed = zlib.compress(data)
            if len(compressed) < len(data):
                data = compressed
        
        # Send header
        header = len(data).to_bytes(4, byteorder='big')
        await self.write(header + data)

class AsyncGhostServer:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.server = None
        self.connections = []
        self.lock = asyncio.Lock()
    
    async def handle_connection(self, reader, writer):
        """Handle incoming connections"""
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")
        
        conn = AsyncGhostConnection(reader, writer)
        
        async with self.lock:
            self.connections.append(conn)
        
        try:
            while not conn.closed:
                # Receive data
                data = await conn.recv()
                
                # Process data
                # This is where you would handle the RPC logic
                logger.debug(f"Received data: {len(data)} bytes")
                
                # Echo back for testing
                await conn.send(data)
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
        finally:
            await conn.close()
            async with self.lock:
                if conn in self.connections:
                    self.connections.remove(conn)
            logger.info(f"Connection from {addr} closed")
    
    async def start(self):
        """Start the server"""
        self.server = await asyncio.start_server(
            self.handle_connection,
            self.host,
            self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f"Async server started on {addr}")
        
        async with self.server:
            await self.server.serve_forever()
    
    async def stop(self):
        """Stop the server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("Async server stopped")

class AsyncGhostClient:
    def __init__(self, host='127.0.0.1', port=4444):
        self.host = host
        self.port = port
        self.conn = None
    
    async def connect(self):
        """Connect to the server"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=10
            )
            self.conn = AsyncGhostConnection(reader, writer)
            logger.info(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    async def send(self, data):
        """Send data to the server"""
        if not self.conn or self.conn.closed:
            raise ConnectionError("Not connected")
        await self.conn.send(data)
    
    async def recv(self):
        """Receive data from the server"""
        if not self.conn or self.conn.closed:
            raise ConnectionError("Not connected")
        return await self.conn.recv()
    
    async def close(self):
        """Close the connection"""
        if self.conn:
            await self.conn.close()
            self.conn = None

if __name__ == '__main__':
    # Test server
    async def test_server():
        server = AsyncGhostServer()
        await server.start()
    
    # Test client
    async def test_client():
        client = AsyncGhostClient()
        if await client.connect():
            # Send test data
            test_data = b'Hello, async world!'
            await client.send(test_data)
            
            # Receive response
            response = await client.recv()
            print(f"Received response: {response}")
            
            # Close connection
            await client.close()
    
    # Run both server and client
    async def main():
        # Start server in background
        server_task = asyncio.create_task(test_server())
        
        # Wait a bit for server to start
        await asyncio.sleep(0.5)
        
        # Run client
        await test_client()
        
        # Stop server
        # Note: In real usage, you would have a way to stop the server gracefully
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
    
    asyncio.run(main())