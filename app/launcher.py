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
    _open_in_terminal(ssh_cmd)


def launch_ssh_command(
    address: str,
    port: int,
    username: str | None,
    command: str,
) -> None:
    """Open a terminal that runs a single command over SSH and stays open.

    The terminal window is kept open after the command finishes so the
    user can review output (and optionally trigger a re-run).
    """
    if not command.strip():
        raise ValueError("命令为空")
    target = f"{username}@{address}" if username else address
    # Quote the remote command so the local shell does not split it.
    quoted_remote = command.replace('"', '\\"')
    ssh_cmd = f'ssh -p {port} {shlex.quote(target)} "{quoted_remote}"'
    _open_in_terminal(ssh_cmd, keep_open=True)


def _open_in_terminal(cmd_line: str, keep_open: bool = True) -> None:
    """Open ``cmd_line`` in a new terminal window cross-platform."""
    if _is_windows():
        # /k keeps the window open; /c closes after exit.
        flag = "/k" if keep_open else "/c"
        subprocess.Popen(
            ["cmd", "/c", "start", "cmd", flag, cmd_line],
            shell=False,
        )
        return
    # Linux / macOS best effort.
    if keep_open:
        # Append a `; echo; read -p ...` so the user can read output.
        wrapped = f'{cmd_line}; echo; read -p "Press Enter to close..." _'
    else:
        wrapped = cmd_line
    for term in ("x-terminal-emulator", "gnome-terminal", "konsole", "xterm"):
        try:
            subprocess.Popen([term, "-e", "bash", "-c", wrapped])
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
