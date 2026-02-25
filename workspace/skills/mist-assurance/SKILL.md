---
name: mist-assurance
description: "Juniper Mist assurance triage - review site alarms and stats to identify WLAN/WAN access problems before deeper troubleshooting."
user-invocable: true
metadata:
  { "openclaw": { "requires": { "bins": ["python3"], "env": ["MIST_MCP_SCRIPT", "MIST_API_TOKEN", "MCP_CALL"] } } }
---

# Juniper Mist Assurance Triage

Use this skill to quickly assess **site health and alarms** in Mist.

## MCP Invocation

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" TOOL_NAME 'ARGS_JSON'
```

## Triage Sequence

1. Run `mist_get_site_stats` for the target site.
2. Run `mist_get_alarms` (default limit 20; increase for active incidents).
3. Sort alarms by severity and recency.
4. Correlate alarm categories with device inventory from `mist-inventory`.

## Severity Guidance

- **CRITICAL**: AP/switch/gateway offline clusters, auth failures with broad blast radius
- **WARNING**: localized AP degradation, uplink instability on a subset of devices
- **INFO**: transient issues already auto-resolved

## Example Call

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" mist_get_alarms '{"site_id":"<SITE_ID>","limit":50}'
```
