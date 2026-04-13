#!/usr/bin/env python3
"""Run a compile command and notify when it completes."""

from __future__ import annotations

import argparse
import platform
import shlex
import subprocess
import sys
import time
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a command, stream output, and send a desktop notification when it finishes.",
    )
    parser.add_argument(
        "--cmd",
        required=True,
        help="Compile command to run, e.g. 'cargo build' or 'npm run build'.",
    )
    parser.add_argument(
        "--name",
        default="Compile Agent",
        help="Name used in notifications.",
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Run command via shell. Enabled automatically for string commands.",
    )
    parser.add_argument(
        "--bell",
        action="store_true",
        help="Play a terminal bell when compilation finishes.",
    )
    return parser.parse_args()


def send_notification(title: str, message: str) -> None:
    system = platform.system().lower()

    try:
        if "darwin" in system:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=False)
        elif "linux" in system:
            subprocess.run(["notify-send", title, message], check=False)
        elif "windows" in system:
            ps = (
                "Add-Type -AssemblyName System.Windows.Forms;"
                f"[System.Windows.Forms.MessageBox]::Show('{message}','{title}')"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)
    except FileNotFoundError:
        # Notification utility missing on this system.
        pass


def run_command(cmd: str, use_shell: bool) -> int:
    start = time.time()
    popen_args: List[str] | str = cmd if use_shell else shlex.split(cmd)

    process = subprocess.Popen(
        popen_args,
        shell=use_shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")

    process.wait()
    duration = time.time() - start
    status = "succeeded" if process.returncode == 0 else "failed"
    return process.returncode, duration, status


def main() -> int:
    args = parse_args()
    use_shell = args.shell or isinstance(args.cmd, str)

    return_code, duration, status = run_command(args.cmd, use_shell)
    message = f"Build {status} in {duration:.1f}s (exit code {return_code})."
    print(f"\n[{args.name}] {message}")

    send_notification(args.name, message)
    if args.bell:
        sys.stdout.write("\a")
        sys.stdout.flush()

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
