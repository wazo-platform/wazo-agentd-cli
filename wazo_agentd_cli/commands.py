# Copyright 2012-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from operator import attrgetter

from cliff.command import Command


class AddAgentToQueueCommand(Command):
    """Add agent to queue"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_id', type=int, help='Agent ID')
        parser.add_argument('queue_id', type=int, help='Queue ID')
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.add_agent_to_queue(
            parsed_args.agent_id, parsed_args.queue_id
        )


class RemoveAgentFromQueueCommand(Command):
    """Remove agent from queue"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_id', type=int, help='Agent ID')
        parser.add_argument('queue_id', type=int, help='Queue ID')
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.remove_agent_from_queue(
            parsed_args.agent_id, parsed_args.queue_id
        )


class LoginCommand(Command):
    """Login agent"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        parser.add_argument('extension', help='Extension')
        parser.add_argument('context', help='Context')
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.login_agent_by_number(
            parsed_args.agent_number, parsed_args.extension, parsed_args.context
        )


class LogoffCommand(Command):
    """Logoff agent"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'agent_number', help='Agent number or "all" to logoff all agents'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.agent_number == 'all':
            self.app.client.agents.logoff_all_agents()
        else:
            self.app.client.agents.logoff_agent_by_number(parsed_args.agent_number)


class RelogAllCommand(Command):
    """Relog all currently logged agents"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--timeout', type=int, default=None, help='Timeout in seconds'
        )
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.relog_all_agents(
            recurse=True, timeout=parsed_args.timeout
        )


class PauseCommand(Command):
    """Pause agent"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.pause_agent_by_number(parsed_args.agent_number)


class UnpauseCommand(Command):
    """Unpause agent"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        return parser

    def take_action(self, parsed_args):
        self.app.client.agents.unpause_agent_by_number(parsed_args.agent_number)


class StatusCommand(Command):
    """Get status of agent"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'agent_number', nargs='?', default=None, help='Agent number'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.agent_number is None:
            agent_statuses = self.app.client.agents.get_agent_statuses(recurse=True)
            for agent_status in sorted(agent_statuses, key=attrgetter('number')):
                _print_agent_status(agent_status)
        else:
            agent_status = self.app.client.agents.get_agent_status_by_number(
                parsed_args.agent_number
            )
            _print_agent_status(agent_status)


def _print_agent_status(agent_status):
    print(f'Agent/{agent_status.number} (ID {agent_status.id})')
    print(f'    logged: {agent_status.logged}')
    if agent_status.logged:
        print(f'    extension: {agent_status.extension}')
        print(f'    context: {agent_status.context}')
        print(f'    state interface: {agent_status.state_interface}')
