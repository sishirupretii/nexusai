"""
nexusai CLI entry point.

Usage:
    nexusai setup          — interactive first-time configuration wizard
    nexusai start          — one-click start (proxy + optional RL training)
    nexusai stop           — stop a running nexusai instance
    nexusai status         — check whether nexusai is running
    nexusai config KEY VAL — set a config value (e.g. rl.enabled true)
    nexusai config show    — show current config
"""

from __future__ import annotations

import sys

try:
    import click
except ImportError:
    print("nexusai requires 'click'. Install it with: pip install click")
    sys.exit(1)

from .config_store import CONFIG_FILE, ConfigStore


@click.group()
def nexusai():
    """nexusai — OpenClaw skill injection and RL training."""


@nexusai.command()
def setup():
    """Interactive first-time configuration wizard."""
    from .setup_wizard import SetupWizard
    SetupWizard().run()


@nexusai.command()
@click.option(
    "--mode",
    type=click.Choice(["skills_only", "rl"]),
    default=None,
    help="Override operating mode for this session.",
)
@click.option(
    "--port",
    type=int,
    default=None,
    help="Override proxy port for this session.",
)
def start(mode: str | None, port: int | None):
    """Start nexusai (proxy + optional RL training)."""
    import asyncio
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    cs = ConfigStore()
    if not cs.exists():
        click.echo(
            "No config found. Run 'nexusai setup' first.",
            err=True,
        )
        sys.exit(1)

    # Session-level overrides (don't persist)
    if mode or port:
        data = cs.load()
        if mode:
            data["mode"] = mode
        if port:
            data.setdefault("proxy", {})["port"] = port
        # Use an in-memory store for this session
        from .config_store import ConfigStore as _CS
        import tempfile, os, yaml
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        )
        yaml.dump(data, tmp)
        tmp.close()
        cs = _CS(config_file=__import__("pathlib").Path(tmp.name))

    from .launcher import nexusaiLauncher
    launcher = nexusaiLauncher(cs)
    try:
        asyncio.run(launcher.start())
    except KeyboardInterrupt:
        click.echo("\nInterrupted — stopping nexusai.")
        launcher.stop()


@nexusai.command()
def stop():
    """Stop a running nexusai instance."""
    import os
    import signal
    from pathlib import Path

    pid_file = Path.home() / ".nexusai" / "nexusai.pid"
    if not pid_file.exists():
        click.echo("nexusai is not running (no PID file found).")
        return
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink(missing_ok=True)
        click.echo(f"Sent SIGTERM to PID {pid}.")
    except ProcessLookupError:
        click.echo("Process not found — cleaning up stale PID file.")
        pid_file.unlink(missing_ok=True)
    except Exception as e:
        click.echo(f"Error stopping nexusai: {e}", err=True)


@nexusai.command()
def status():
    """Check whether nexusai is running."""
    import os
    from pathlib import Path

    pid_file = Path.home() / ".nexusai" / "nexusai.pid"
    if not pid_file.exists():
        click.echo("nexusai: not running")
        return

    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)  # check if process exists
    except (ProcessLookupError, ValueError):
        click.echo("nexusai: not running (stale PID file)")
        pid_file.unlink(missing_ok=True)
        return

    # Try health check
    cs = ConfigStore()
    port = cs.get("proxy.port") or 30000
    try:
        import urllib.request
        with urllib.request.urlopen(
            f"http://localhost:{port}/healthz", timeout=2
        ) as resp:
            healthy = resp.status == 200
    except Exception:
        healthy = False

    mode = cs.get("mode") or "?"
    if healthy:
        click.echo(f"nexusai: running  (PID={pid}, mode={mode}, proxy=:{port})")
    else:
        click.echo(f"nexusai: starting (PID={pid}, mode={mode}, proxy=:{port})")


@nexusai.command(name="config")
@click.argument("key_or_action")
@click.argument("value", required=False)
def config_cmd(key_or_action: str, value: str | None):
    """Get or set a config value.

    Examples:\n
      nexusai config show\n
      nexusai config rl.enabled true\n
      nexusai config proxy.port 30001
    """
    cs = ConfigStore()
    if key_or_action == "show":
        if not cs.exists():
            click.echo("No config file found. Run 'nexusai setup' first.")
            return
        click.echo(f"Config file: {CONFIG_FILE}\n")
        click.echo(cs.describe())
        return

    if value is None:
        # Get mode
        result = cs.get(key_or_action)
        if result is None:
            click.echo(f"{key_or_action}: (not set)")
        else:
            click.echo(f"{key_or_action}: {result}")
        return

    cs.set(key_or_action, value)
    click.echo(f"Set {key_or_action} = {cs.get(key_or_action)}")
