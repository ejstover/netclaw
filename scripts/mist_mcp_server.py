#!/usr/bin/env python3
"""Simple Juniper Mist MCP server (read-only)."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("juniper-mist-mcp")


class MistClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("MIST_BASE_URL", "https://api.mist.com/api/v1").rstrip("/")
        self.token = os.getenv("MIST_API_TOKEN", "").strip()
        if not self.token:
            raise ValueError("MIST_API_TOKEN is required")

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers={"Authorization": f"Token {self.token}", "Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}


@mcp.tool()
def mist_get_self() -> Dict[str, Any]:
    """Return the authenticated Mist user context."""
    return MistClient().request("GET", "self")


@mcp.tool()
def mist_get_orgs() -> Any:
    """List organizations visible to the API token."""
    return MistClient().request("GET", "orgs")


@mcp.tool()
def mist_get_sites(org_id: str) -> Any:
    """List all sites for a Mist organization."""
    return MistClient().request("GET", f"orgs/{org_id}/sites")


@mcp.tool()
def mist_get_devices(site_id: str, type: Optional[str] = None) -> Any:
    """List wired/wireless devices in a site. Optional type filter (ap, switch, gateway)."""
    params: Dict[str, Any] = {}
    if type:
        params["type"] = type
    return MistClient().request("GET", f"sites/{site_id}/devices", params=params or None)


@mcp.tool()
def mist_get_alarms(site_id: str, limit: int = 20) -> Any:
    """List active/recent site alarms, newest first."""
    return MistClient().request("GET", f"sites/{site_id}/alarms/search", params={"limit": limit})


@mcp.tool()
def mist_get_site_stats(site_id: str) -> Any:
    """Return high-level site statistics (clients, APs, switches, gateways, health)."""
    return MistClient().request("GET", f"sites/{site_id}/stats")


if __name__ == "__main__":
    mcp.run(transport="stdio")
