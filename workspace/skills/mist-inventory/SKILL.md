---
name: mist-inventory
description: "Juniper Mist inventory and topology context - list orgs/sites, enumerate APs/switches/gateways, and collect high-level site stats for wireless and wired operations."
user-invocable: true
metadata:
  { "openclaw": { "requires": { "bins": ["python3"], "env": ["MIST_MCP_SCRIPT", "MIST_API_TOKEN", "MCP_CALL"] } } }
---

# Juniper Mist Inventory

Use this skill for **read-only Mist inventory** discovery following the same MCP pattern used in other NetClaw domains.

## MCP Invocation

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" TOOL_NAME 'ARGS_JSON'
```

## Core Workflows

1. **Discover tenant scope**
   - `mist_get_self` to validate API auth context
   - `mist_get_orgs` to list available organizations

2. **Site inventory**
   - `mist_get_sites` with `org_id`
   - For each site, gather:
     - `mist_get_site_stats`
     - `mist_get_devices` (`type=ap`, `type=switch`, `type=gateway`)

3. **Output expectations**
   - Provide per-site counts of AP/switch/gateway/client health context
   - Flag sites with zero infrastructure devices or missing stats
   - Recommend follow-up with `mist-assurance` when alarms exist

## Example Calls

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" mist_get_orgs '{}'
```

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" mist_get_sites '{"org_id":"<ORG_ID>"}'
```

```bash
MIST_API_TOKEN=$MIST_API_TOKEN python3 $MCP_CALL "python3 -u $MIST_MCP_SCRIPT" mist_get_devices '{"site_id":"<SITE_ID>","type":"ap"}'
```
