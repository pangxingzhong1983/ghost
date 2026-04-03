#!/usr/bin/env python3
"""
测试 WebSocket 连接和 WebUI 功能
"""

import asyncio
import websockets
import json
import sys

async def test_websocket():
    """测试 WebSocket 连接"""
    uri = "ws://localhost:8766"
    print(f"[*] Connecting to WebSocket at {uri}...")

    try:
        async with websockets.connect(uri) as websocket:
            print("[+] Connected successfully!")

            # 接收欢迎消息
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"[+] Received welcome: {welcome_data}")

            # 测试获取会话列表
            await websocket.send(json.dumps({
                "event": "get_sessions"
            }))
            sessions = await websocket.recv()
            print(f"[+] Sessions response: {sessions[:200]}...")

            # 测试获取监听器列表
            await websocket.send(json.dumps({
                "event": "get_listeners"
            }))
            listeners = await websocket.recv()
            print(f"[+] Listeners response: {listeners[:200]}...")

            print("\n[+] All WebSocket tests passed!")
            return True

    except Exception as e:
        print(f"[-] WebSocket test failed: {e}")
        return False

def test_http():
    """测试 HTTP 服务"""
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:8081", timeout=5) as resp:
            if resp.status == 200:
                html = resp.read().decode('utf-8')
                print("[+] WebUI HTTP server responding (200 OK)")
                if "ghost-webui" in html or "root" in html:
                    print("[+] WebUI HTML content looks correct")
                return True
    except Exception as e:
        print(f"[-] HTTP test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Ghost C2 Deployment Test ===\n")

    # Test HTTP
    print("[1/2] Testing HTTP (WebUI)...")
    http_ok = test_http()

    # Test WebSocket
    print("\n[2/2] Testing WebSocket...")
    ws_ok = asyncio.run(test_websocket())

    # Summary
    print("\n=== Test Summary ===")
    print(f"HTTP/WebUI: {'✅ PASS' if http_ok else '❌ FAIL'}")
    print(f"WebSocket:  {'✅ PASS' if ws_ok else '❌ FAIL'}")

    if http_ok and ws_ok:
        print("\n🎉 All services are working correctly!")
        sys.exit(0)
    else:
        print("\n⚠️ Some services failed. Check logs with: docker-compose logs")
        sys.exit(1)
