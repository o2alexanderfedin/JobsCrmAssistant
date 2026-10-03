"""Start the real server in a child process and check that it answers.

The other tests build the app inside the test process. This one runs
uvicorn the way a person would, so an app that cannot start (a broken
import, a settings error at import time) fails the suite.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

APP = "jobs_crm_assistant.api.app:app"
DEADLINE_SECONDS = 20.0
LISTENING = re.compile(r"Uvicorn running on http://127\.0\.0\.1:(\d+)")


def _wait_for_port(log: Path, server: "subprocess.Popen[bytes]") -> int:
    """Return the port uvicorn reports, or fail with the server's log."""
    deadline = time.monotonic() + DEADLINE_SECONDS
    while time.monotonic() < deadline:
        text = log.read_text(encoding="utf-8", errors="replace")
        match = LISTENING.search(text)
        if match:
            return int(match.group(1))
        if server.poll() is not None:
            raise AssertionError(
                f"server exited with code {server.returncode}:\n{text}"
            )
        time.sleep(0.1)
    raise AssertionError(f"server did not start in time:\n{log.read_text()}")


def test_server_starts_and_answers_health(tmp_path: Path) -> None:
    """Uvicorn must start the app with a fake key and serve /health."""
    env = dict(os.environ)
    env["OPENAI_API_KEY"] = "sk-test-not-a-real-key"
    env.pop("CORS_ORIGINS", None)
    log = tmp_path / "server.log"

    with log.open("wb") as out:
        # Port 0: the system picks a free port, so parallel runs never
        # collide; cwd=tmp_path keeps a developer's .env out of the test.
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", APP]
            + ["--host", "127.0.0.1", "--port", "0"],
            cwd=tmp_path,
            env=env,
            stdout=out,
            stderr=subprocess.STDOUT,
        )
    try:
        port = _wait_for_port(log, server)
        # No proxy: an HTTP_PROXY in the environment must not catch this.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        url = f"http://127.0.0.1:{port}/health"
        try:
            with opener.open(url, timeout=5) as response:
                status = response.status
                body = json.loads(response.read())
        except OSError as error:
            raise AssertionError(
                f"GET /health failed: {error}\n{log.read_text()}"
            ) from error
        assert status == 200, log.read_text()
        assert body == {"status": "healthy"}, log.read_text()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


def test_readme_documents_the_install_and_start_commands() -> None:
    """The README must give the commands this file proves to work."""
    readme = (Path(__file__).resolve().parent.parent / "README.md").read_text(
        encoding="utf-8"
    )

    assert 'pip install -e ".[dev]"' in readme
    assert f"uvicorn {APP}" in readme
