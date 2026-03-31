from __future__ import annotations

from typing import Any

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado.web

from .schema import ExecuteRequest
from .routing import resolve_mode_for_user
from .claude_local_runner import run_local_claude
from .claude_remote_client import run_remote_claude


class ExecuteHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self):
        body: dict[str, Any] = self.get_json_body() or {}
        req = ExecuteRequest(**body)

        user = self.current_user
        username = user.username if hasattr(user, "username") else str(user)

        mode = resolve_mode_for_user(username, req.jcm_mode)

        if mode == "remote_mgt":
            result = run_remote_claude(
                req,
                remote_broker_url=req.remote_broker_url,
            )
        else:
            result = run_local_claude(
                req,
                executable_path=req.claude_executable_path,
            )

        self.finish(result.model_dump())


def _jupyter_server_extension_points():
    return [{"module": "magiclaude"}]


def _load_jupyter_server_extension(server_app):
    web_app = server_app.web_app
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "claude-notebook", "execute")
    web_app.add_handlers(host_pattern, [(route_pattern, ExecuteHandler)])
    server_app.log.info("Registered magiclaude endpoint at /claude-notebook/execute")
