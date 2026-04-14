# wazo-agentd-cli

A CLI program to interact with wazo-agentd

## Usage

```shell
$ wazo-agentd-cli --host example.org status 1004
Agent/1004 (ID 4)
    logged: False
$ wazo-agentd-cli login 1004 1004 default
$ wazo-agentd-cli status 1004
Agent/1004 (ID 4)
    logged: True
    extension: 1004
    context: default
    state interface: SIP/alice
```

## Commands

- `add <agent_id> <queue_id>` - Add agent to queue
- `remove <agent_id> <queue_id>` - Remove agent from queue
- `login <agent_number> <extension> <context>` - Login agent
- `logoff <agent_number|all>` - Logoff agent or all agents
- `relog all [--timeout <seconds>]` - Relog all currently logged agents
- `pause <agent_number>` - Pause agent
- `unpause <agent_number>` - Unpause agent
- `status [<agent_number>]` - Get status of one or all agents

## Output formats

The `status` command supports cliff's `-f` flag for alternative output formats:

```shell
wazo-agentd-cli status -f table
wazo-agentd-cli status -f json
wazo-agentd-cli status -f csv
wazo-agentd-cli status -f yaml
```

The default format is the legacy text format.
