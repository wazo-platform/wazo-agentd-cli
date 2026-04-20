# Copyright 2012-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
from collections.abc import Sequence
from operator import attrgetter
from typing import Any

from cliff.command import Command
from cliff.lister import Lister


class AddAgentToQueueCommand(Command):
    """Add agent to queue"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_id', type=int, help='Agent ID')
        parser.add_argument('queue_id', type=int, help='Queue ID')
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.add_agent_to_queue(
            parsed_args.agent_id, parsed_args.queue_id
        )


class RemoveAgentFromQueueCommand(Command):
    """Remove agent from queue"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_id', type=int, help='Agent ID')
        parser.add_argument('queue_id', type=int, help='Queue ID')
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.remove_agent_from_queue(
            parsed_args.agent_id, parsed_args.queue_id
        )


class LoginCommand(Command):
    """Login agent"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        parser.add_argument('extension', help='Extension')
        parser.add_argument('context', help='Context')
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.login_agent_by_number(
            parsed_args.agent_number, parsed_args.extension, parsed_args.context
        )


class LogoffCommand(Command):
    """Logoff agent"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'agent_number', help='Agent number or "all" to logoff all agents'
        )
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        if parsed_args.agent_number == 'all':
            self.app.client.agents.logoff_all_agents()
        else:
            self.app.client.agents.logoff_agent_by_number(parsed_args.agent_number)


class RelogAllCommand(Command):
    """Relog all currently logged agents"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--timeout', type=int, default=None, help='Timeout in seconds'
        )
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.relog_all_agents(
            recurse=True, timeout=parsed_args.timeout
        )


class PauseCommand(Command):
    """Pause agent"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.pause_agent_by_number(parsed_args.agent_number)


class UnpauseCommand(Command):
    """Unpause agent"""

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('agent_number', help='Agent number')
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client.agents.unpause_agent_by_number(parsed_args.agent_number)


class StatusCommand(Lister):
    """Get status of agent"""

    COLUMNS = (
        'number',
        'id',
        'logged',
        'extension',
        'context',
        'state_interface',
        'queues',
    )

    @property
    def formatter_default(self) -> str:
        return 'legacy'

    def get_parser(self, *args: Any, **kwargs: Any) -> argparse.ArgumentParser:
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'agent_number', nargs='?', default=None, help='Agent number'
        )
        return parser

    def take_action(
        self, parsed_args: argparse.Namespace
    ) -> tuple[Sequence[str], list[tuple]]:
        if parsed_args.agent_number is None:
            agent_statuses = self.app.client.agents.get_agent_statuses(recurse=True)
            statuses = sorted(agent_statuses, key=attrgetter('number'))
        else:
            status = self.app.client.agents.get_agent_status_by_number(
                parsed_args.agent_number
            )
            statuses = [status]
        rows = [
            (
                s.number,
                s.id,
                s.logged,
                s.extension if s.logged else '',
                s.context if s.logged else '',
                s.state_interface if s.logged else '',
                s.queues,
            )
            for s in statuses
        ]
        return self.COLUMNS, rows
