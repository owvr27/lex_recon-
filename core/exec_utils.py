from __future__ import annotations
import subprocess
import shlex
import time
from dataclasses import dataclass
from typing import Optional, Sequence

@dataclass
class CmdResult:
    cmd: str
    returncode: int
    duration_s: float
    stdout: str | None = None
    stderr: str | None = None
    timed_out: bool = False

def run_cmd(
    cmd: str | Sequence[str],
    *,
    shell: bool = False,
    timeout_s: Optional[int] = None,
    capture: bool = False,
    quiet: bool = False,
    env: dict | None = None,
) -> CmdResult:
    start = time.time()
    if isinstance(cmd, (list, tuple)):
        cmd_str = " ".join(shlex.quote(str(c)) for c in cmd)
    else:
        cmd_str = cmd
    try:
        if capture:
            proc = subprocess.run(
                cmd,
                shell=shell,
                timeout=timeout_s,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            return CmdResult(cmd_str, proc.returncode, time.time() - start, proc.stdout, proc.stderr, False)
        else:
            # default to discarding stderr unless caller wants it
            stderr = subprocess.DEVNULL if quiet else None
            proc = subprocess.run(
                cmd,
                shell=shell,
                timeout=timeout_s,
                check=False,
                text=True,
                stdout=None,
                stderr=stderr,
                env=env,
            )
            return CmdResult(cmd_str, proc.returncode, time.time() - start, None, None, False)
    except subprocess.TimeoutExpired:
        return CmdResult(cmd_str, 124, time.time() - start, None, None, True)
