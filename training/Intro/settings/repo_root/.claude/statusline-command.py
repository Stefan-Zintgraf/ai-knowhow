#!/usr/bin/env python3
"""ec-embedded team status line for Claude Code (Windows/Linux)."""
import json
import os
import subprocess
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    model = (data.get("model") or {}).get("display_name") or "Claude"

    ctx = (data.get("context_window") or {}).get("remaining_percentage")
    ctx_str = f"ctx:{ctx:.0f}%" if isinstance(ctx, (int, float)) else "ctx:--"

    rate_str = ""
    five_h = ((data.get("rate_limits") or {}).get("five_hour") or {}).get("used_percentage")
    if isinstance(five_h, (int, float)):
        rate_str = f" | 5h:{five_h:.0f}% used"

    workspace = data.get("workspace") or {}
    cwd = workspace.get("current_dir") or data.get("cwd") or ""
    repo_root = workspace.get("project_dir") or ""
    if repo_root and cwd and cwd.startswith(repo_root):
        rel = cwd[len(repo_root):] or "/"
        dir_str = rel.replace("\\", "/")
    else:
        dir_str = cwd.replace("\\", "/")

    branch_str = ""
    if cwd:
        try:
            out = subprocess.run(
                ["git", "-C", cwd, "--no-optional-locks", "symbolic-ref", "--short", "HEAD"],
                capture_output=True, text=True, timeout=2,
            )
            if out.returncode == 0 and out.stdout.strip():
                branch_str = f" | {out.stdout.strip()}"
        except Exception:
            pass

    vim_str = ""
    vim_mode = (data.get("vim") or {}).get("mode")
    if vim_mode:
        vim_str = f" | [{vim_mode}]"

    sys.stdout.write(f"{model} | {ctx_str}{rate_str} | {dir_str}{branch_str}{vim_str}")


if __name__ == "__main__":
    main()
