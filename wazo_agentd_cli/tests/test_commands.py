# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from argparse import Namespace
from typing import Any
from unittest.mock import Mock

from wazo_agentd_cli.commands import (
    LoginCommand,
    LogoffCommand,
    RelogAllCommand,
    StatusCommand,
)


class TestLoginCommand:
    def test_take_action(self) -> None:
        app = Mock()
        cmd = LoginCommand(app, None)
        parsed_args = Namespace(
            agent_number='1001', extension='1001', context='default'
        )
        cmd.take_action(parsed_args)
        app.client.agents.login_agent_by_number.assert_called_once_with(
            '1001', '1001', 'default'
        )


class TestLogoffCommand:
    def test_logoff_by_number(self) -> None:
        app = Mock()
        cmd = LogoffCommand(app, None)
        parsed_args = Namespace(agent_number='1001')
        cmd.take_action(parsed_args)
        app.client.agents.logoff_agent_by_number.assert_called_once_with('1001')

    def test_logoff_all(self) -> None:
        app = Mock()
        cmd = LogoffCommand(app, None)
        parsed_args = Namespace(agent_number='all')
        cmd.take_action(parsed_args)
        app.client.agents.logoff_all_agents.assert_called_once()


class TestRelogAllCommand:
    def test_with_timeout(self) -> None:
        app = Mock()
        cmd = RelogAllCommand(app, None)
        parsed_args = Namespace(timeout=30)
        cmd.take_action(parsed_args)
        app.client.agents.relog_all_agents.assert_called_once_with(
            recurse=True, timeout=30
        )

    def test_without_timeout(self) -> None:
        app = Mock()
        cmd = RelogAllCommand(app, None)
        parsed_args = Namespace(timeout=None)
        cmd.take_action(parsed_args)
        app.client.agents.relog_all_agents.assert_called_once_with(
            recurse=True, timeout=None
        )


class TestStatusCommand:
    def _make_status(
        self,
        number: str,
        agent_id: int,
        logged: bool,
        extension: str = '',
        context: str = '',
        state_interface: str = '',
        queues: list[dict[str, Any]] | None = None,
    ) -> Mock:
        return Mock(
            number=number,
            id=agent_id,
            logged=logged,
            extension=extension,
            context=context,
            state_interface=state_interface,
            queues=queues or [],
        )

    def test_single_agent_returns_columns_and_row(self) -> None:
        app = Mock()
        queues = [{'id': 1, 'name': 'support', 'logged': True, 'paused': False}]
        status = self._make_status(
            '1001',
            42,
            True,
            extension='1001',
            context='default',
            state_interface='SIP/abc',
            queues=queues,
        )
        app.client.agents.get_agent_status_by_number.return_value = status
        cmd = StatusCommand(app, None)
        parsed_args = Namespace(agent_number='1001')

        columns, rows = cmd.take_action(parsed_args)

        assert columns == (
            'number',
            'id',
            'logged',
            'extension',
            'context',
            'state_interface',
            'queues',
        )
        assert rows == [('1001', 42, True, '1001', 'default', 'SIP/abc', queues)]

    def test_not_logged_agent_has_empty_fields(self) -> None:
        app = Mock()
        status = self._make_status('1002', 43, False)
        app.client.agents.get_agent_status_by_number.return_value = status
        cmd = StatusCommand(app, None)
        parsed_args = Namespace(agent_number='1002')

        _, rows = cmd.take_action(parsed_args)

        assert rows == [('1002', 43, False, '', '', '', [])]

    def test_all_agents_sorted_by_number(self) -> None:
        app = Mock()
        s1 = self._make_status('1002', 43, False)
        s2 = self._make_status(
            '1001',
            42,
            True,
            extension='1001',
            context='default',
            state_interface='SIP/abc',
        )
        app.client.agents.get_agent_statuses.return_value = [s1, s2]
        cmd = StatusCommand(app, None)
        parsed_args = Namespace(agent_number=None)

        _, rows = cmd.take_action(parsed_args)

        assert rows[0][0] == '1001'
        assert rows[1][0] == '1002'
        app.client.agents.get_agent_statuses.assert_called_once_with(recurse=True)
