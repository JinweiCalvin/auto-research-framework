#!/usr/bin/env python3
"""Start the local research dashboard and open it in the default browser."""
from __future__ import annotations

import socket
import sys
import time
import webbrowser
from urllib.error import HTTPError
from urllib.request import urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "idea2paper" / "frontend" / "server" / "app.py"
HOST = "127.0.0.1"
PORT = 8080


def main() -> int:
    port = PORT
    while port < PORT + 20:
        url = f"http://{HOST}:{port}/"
        try:
            with socket.create_connection((HOST, port), timeout=0.25):
                with urlopen(url, timeout=2) as response:
                    if response.status == 200 and "科研工作台" in response.read(4096).decode("utf-8", errors="replace"):
                        print(f"科研工作台已经在运行：{url}")
                        webbrowser.open(url)
                        return 0
                port += 1
                continue
        except OSError:
            pass
        except HTTPError:
            port += 1
            continue
        command = [sys.executable, str(SERVER), "--host", HOST, "--port", str(port)]
        for _ in range(40):
            try:
                with urlopen(url, timeout=0.5) as response:
                    if response.status == 200 and "科研工作台" in response.read(4096).decode("utf-8", errors="replace"):
                        print(f"科研工作台已启动：{url}")
                        if port != PORT:
                            print(f"端口 {PORT} 被已有服务占用，已安全使用端口 {port}。")
                        webbrowser.open(url)
                        print("保持此启动窗口打开即可使用；关闭窗口会停止本地服务。")
                        import os
                        os.chdir(ROOT / "idea2paper")
                        os.execv(sys.executable, command)
            except OSError:
                time.sleep(0.25)
        port += 1
    print("无法找到可用端口启动工作台。", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
