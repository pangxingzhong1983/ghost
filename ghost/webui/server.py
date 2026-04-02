#!/usr/bin/env python3
import asyncio
import websockets
import json
import subprocess
import os

# 存储会话信息
sessions = {}

async def handle_client(websocket):
    try:
        # 发送欢迎消息
        await websocket.send(json.dumps({
            "event": "welcome",
            "data": {
                "message": "Connected to Ghost WebSocket Server"
            }
        }))
        
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")
            
            if data.get("event") == "auth":
                # 模拟登录验证
                await websocket.send(json.dumps({
                    "event": "auth_response",
                    "data": {
                        "id": data.get("data", {}).get("id"),
                        "success": True,
                        "token": "mock_token"
                    }
                }))
            
            elif data.get("event") == "get_sessions":
                # 模拟返回会话列表
                await websocket.send(json.dumps({
                    "event": "sessions_response",
                    "data": [
                        {"id": "1", "name": "Session 1", "host": "192.168.1.100", "port": 4444, "time": "2024-01-01 12:00:00"},
                        {"id": "2", "name": "Session 2", "host": "192.168.1.101", "port": 4444, "time": "2024-01-01 12:05:00"}
                    ]
                }))
            
            elif data.get("event") == "get_listeners":
                # 模拟返回监听器列表
                await websocket.send(json.dumps({
                    "event": "listeners_response",
                    "data": [
                        {"id": "1", "name": "Listener 1", "host": "0.0.0.0", "port": 4444, "type": "http", "status": "running"},
                        {"id": "2", "name": "Listener 2", "host": "0.0.0.0", "port": 4445, "type": "https", "status": "running"}
                    ]
                }))
            
            elif data.get("event") == "get_payloads":
                # 模拟返回Payload列表
                await websocket.send(json.dumps({
                    "event": "payloads_response",
                    "data": [
                        {"id": "1", "name": "Payload 1", "type": "windows/meterpreter/reverse_tcp", "size": "1024"},
                        {"id": "2", "name": "Payload 2", "type": "linux/x86/meterpreter/reverse_tcp", "size": "980"}
                    ]
                }))
            
            elif data.get("event") == "execute_command":
                # 模拟执行命令
                session_id = data.get("data", {}).get("sessionId")
                command = data.get("data", {}).get("command")
                
                # 模拟命令执行结果
                await websocket.send(json.dumps({
                    "event": "command_result",
                    "data": {
                        "sessionId": session_id,
                        "command": command,
                        "result": f"Executed command: {command}\nMock result output"
                    }
                }))
            
            elif data.get("event") == "get_modules":
                # 模拟返回模块列表
                await websocket.send(json.dumps({
                    "event": "modules_response",
                    "data": [
                        {"id": "1", "name": "bypassuac", "description": "Bypass UAC on Windows systems"},
                        {"id": "2", "name": "getsystem", "description": "Elevate privileges to SYSTEM"},
                        {"id": "3", "name": "mimikatz", "description": "Extract credentials from memory"}
                    ]
                }))
            
            elif data.get("event") == "get_credentials":
                # 模拟返回凭证列表
                await websocket.send(json.dumps({
                    "event": "credentials_response",
                    "data": [
                        {"id": "1", "username": "admin", "password": "password123", "domain": "WORKGROUP"},
                        {"id": "2", "username": "user", "password": "pass123", "domain": "WORKGROUP"}
                    ]
                }))
            
            elif data.get("event") == "get_jobs":
                # 模拟返回作业列表
                await websocket.send(json.dumps({
                    "event": "jobs_response",
                    "data": [
                        {"id": "1", "name": "Job 1", "status": "running", "start_time": "2024-01-01 12:00:00"},
                        {"id": "2", "name": "Job 2", "status": "completed", "start_time": "2024-01-01 11:30:00"}
                    ]
                }))
            
            elif data.get("event") == "get_files":
                # 模拟返回文件列表
                await websocket.send(json.dumps({
                    "event": "files_response",
                    "data": [
                        {"id": "1", "name": "file1.txt", "size": "1024", "path": "/home/user/file1.txt"},
                        {"id": "2", "name": "file2.exe", "size": "10240", "path": "/home/user/file2.exe"}
                    ]
                }))
            
            elif data.get("event") == "command":
                # 处理命令执行
                command = data.get("data", {}).get("command")
                args = data.get("data", {}).get("args", [])
                command_id = data.get("data", {}).get("id")
                
                print(f"Processing command: {command} {args} with id: {command_id}")
                
                # 模拟命令执行结果
                if command == "sessions":
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": [
                                {"id": "1", "name": "Session 1", "host": "192.168.1.100", "port": 4444, "time": "2024-01-01 12:00:00", "platform": "Windows 10"},
                                {"id": "2", "name": "Session 2", "host": "192.168.1.101", "port": 4444, "time": "2024-01-01 12:05:00", "platform": "Linux Ubuntu 20.04"}
                            ]
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending response for sessions: {response}")
                    await websocket.send(response)
                elif command == "listen" and args == ["--list"]:
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": [
                                {"id": "1", "name": "Listener 1", "host": "0.0.0.0", "port": 4444, "type": "http", "status": "running"},
                                {"id": "2", "name": "Listener 2", "host": "0.0.0.0", "port": 4445, "type": "https", "status": "running"}
                            ]
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending response for listen --list: {response}")
                    await websocket.send(response)
                elif command == "creds":
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": [
                                {"id": "1", "username": "admin", "password": "password123", "domain": "WORKGROUP"},
                                {"id": "2", "username": "user", "password": "pass123", "domain": "WORKGROUP"}
                            ]
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending response for creds: {response}")
                    await websocket.send(response)
                elif command == "job" and args == ["list"]:
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": [
                                {"id": "1", "name": "Job 1", "status": "running", "start_time": "2024-01-01 12:00:00"},
                                {"id": "2", "name": "Job 2", "status": "completed", "start_time": "2024-01-01 11:30:00"}
                            ]
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending response for job list: {response}")
                    await websocket.send(response)
                elif command == "payload" and args == ["list"]:
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": [
                                {"id": "1", "name": "Windows Reverse Shell", "type": "exe", "platform": "windows", "arch": "x64", "listener": "HTTP Listener", "status": "generated", "created_at": "2026-03-30 14:00:00", "expires_at": "2026-04-01 14:00:00", "size": "1.2 MB"},
                                {"id": "2", "name": "Linux Reverse Shell", "type": "elf", "platform": "linux", "arch": "x64", "listener": "HTTPS Listener", "status": "used", "created_at": "2026-03-30 13:30:00", "expires_at": "2026-04-01 13:30:00", "size": "800 KB"},
                                {"id": "3", "name": "MacOS Reverse Shell", "type": "macho", "platform": "macos", "arch": "x64", "listener": "HTTP Listener", "status": "expired", "created_at": "2026-03-28 10:00:00", "expires_at": "2026-03-29 10:00:00", "size": "1.5 MB"}
                            ]
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending response for payload list: {response}")
                    await websocket.send(response)
                else:
                    # 其他命令的默认响应
                    response_data = {
                        "event": "command_response",
                        "data": {
                            "id": command_id,
                            "result": f"Executed command: {command} {', '.join(args)}"
                        }
                    }
                    response = json.dumps(response_data)
                    print(f"Sending default response for {command}: {response}")
                    await websocket.send(response)
            
            else:
                # 未知消息类型
                await websocket.send(json.dumps({
                    "event": "error",
                    "data": {
                        "message": "Unknown message type"
                    }
                }))
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "localhost", 8766):
        print("WebSocket server started on ws://localhost:8766")
        await asyncio.Future()  # 保持服务器运行

if __name__ == "__main__":
    asyncio.run(main())