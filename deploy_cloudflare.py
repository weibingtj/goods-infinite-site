#!/usr/bin/env python3
"""
Deploy GOODSINFINITE site to Cloudflare Pages via wrangler (Direct Upload).

Route B: no GitHub needed. Uses the official `wrangler` CLI, which handles the
multipart upload correctly (a hand-rolled multipart was tried earlier and
Cloudflare mis-parsed it, creating empty deployments).

Prereqs (in .deploy.env, never committed):
  CLOUDFLARE_API_TOKEN=cfat_xxx    # scoped: Account>Cloudflare Pages>Edit (+ Zone>Dns>Edit for custom domain)
  CLOUDFLARE_ACCOUNT_ID=xxxx       # dashboard bottom-right
  PROJECT_NAME=goods-infinite-site

Usage:
  python deploy_cloudflare.py            # build insight articles + deploy
  python deploy_cloudflare.py --dry-run  # build only, no upload
"""
import os
import sys
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".deploy.env"


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    dry_run = "--dry-run" in sys.argv
    env = load_env()
    # expose token/account for wrangler (it reads these from the environment)
    for k in ("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID", "PROJECT_NAME"):
        if env.get(k):
            os.environ[k] = env[k]

    print("[1/2] Building insight articles...")
    subprocess.run([sys.executable, "build_insights.py"], cwd=str(HERE), check=True)
    print("      build done.")

    if dry_run:
        print("[2/2] --dry-run: skipping deploy.")
        return

    name = env.get("PROJECT_NAME") or "goods-infinite-site"
    print(f"[2/2] Deploying to Cloudflare Pages project '{name}' via wrangler...")

    # Resolve wrangler runner. On Windows `npx` is a .cmd that only runs via the
    # shell, and a managed Node install may not be on PATH inside subprocess.
    npx = os.environ.get("NPM_EXECUTABLE")
    if not npx:
        candidate = (HERE.parent / ".workbuddy" / "binaries" / "node"
                     / "versions" / "22.22.2" / "npx.cmd")
        fallback = r"C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\npx.cmd"
        if candidate.exists():
            npx = str(candidate)
        elif os.path.exists(fallback):
            npx = fallback
        else:
            npx = "npx"
    print(f"      using runner: {npx}")

    cmd = (f'"{npx}" --yes wrangler@latest pages deploy . '
           f'--project-name {name} --branch main --commit-dirty=true')
    rc = subprocess.run(cmd, cwd=str(HERE), shell=True).returncode
    if rc != 0:
        print("Deploy failed. See wrangler output above.")
        sys.exit(rc)
    print(f"Done. Live at https://{name}.pages.dev")


if __name__ == "__main__":
    main()
