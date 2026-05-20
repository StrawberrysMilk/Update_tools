"""One-click launchers for RDP / SSH / browser / custom commands.

Skeleton stage: minimal, cross-platform-aware implementations.
Will be extended (cmdkey credential staging, Windows Terminal preference,
SSH key support, etc.) in subsequent iterations.
"""
from __future__ import annotations

import platform
import shlex
import subprocess
import webbrowser


def _is_windows() -> bool:
    return platform.system() == "Windows"


def launch_rdp(address: str, username: str | None = None, password: str | None = None) -> None:
    """Open mstsc on Windows. Optionally cache credentials with cmdkey."""
    if not _is_windows():
        raise RuntimeError("RDP 启动需要 Windows 系统 (mstsc)")
    host = address.split(":")[0] if address else ""
    if username and password and host:
        # Cache credential so mstsc does not re-prompt. (NB: persists in
        # Windows Credential Manager until removed.)
        subprocess.run(
            [
                "cmdkey",
                f"/generic:TERMSRV/{host}",
                f"/user:{username}",
                f"/pass:{password}",
            ],
            check=False,
            capture_output=True,
        )
    subprocess.Popen(["mstsc", f"/v:{address}"])


def launch_ssh(address: str, port: int = 22, username: str | None = None) -> None:
    """Open an SSH session in a new terminal window."""
    target = f"{username}@{address}" if username else address
    ssh_cmd = f"ssh -p {port} {shlex.quote(target)}"
    if _is_windows():
        # Open a new cmd window that runs ssh (kept open after exit).
        subprocess.Popen(
            ["cmd", "/c", "start", "cmd", "/k", ssh_cmd],
            shell=False,
        )
    else:
        # Best-effort terminal emulator on Linux/macOS.
        for term in ("x-terminal-emulator", "gnome-terminal", "konsole", "xterm"):
            try:
                subprocess.Popen([term, "-e", ssh_cmd])
                return
            except FileNotFoundError:
                continue
        raise RuntimeError("未找到可用的终端模拟器")


def launch_browser(url: str) -> None:
    webbrowser.open(url)


def launch_custom(command: str) -> None:
    """Run an arbitrary user-defined command (e.g. iNode 客户端 path)."""
    if _is_windows():
        subprocess.Popen(command, shell=True)
    else:
        subprocess.Popen(shlex.split(command))
