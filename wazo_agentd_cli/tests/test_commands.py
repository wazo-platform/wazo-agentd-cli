# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import Namespace
from unittest.mock import Mock

from wazo_agentd_cli.commands import (
    LoginCommand,
    LogoffCommand,
    RelogAllCommand,
    StatusCommand,
    _print_agent_status,
)


class TestPrintAgentStatus:
    def test_logged_agent(self, capsys):
        status = Mock(
            number='1001',
            id=42,
            logged=True,
            extension='1001',
            context='default',
            state_interface='SIP/abc',
        )
        _print_agent_status(status)
        output = capsys.readouterr().out
        assert output == (
            'Agent/1001 (ID 42)\n'
            '    logged: True\n'
            '    extension: 1001\n'
            '    context: default\n'
            '    state interface: SIP/abc\n'
        )

    def test_not_logged_agent(self, capsys):
        status = Mock(number='1002', id=43, logged=False)
        _print_agent_status(status)
        output = capsys.readouterr().out
        assert output == ('Agent/1002 (ID 43)\n' '    logged: False\n')


class TestLoginCommand:
    def test_take_action(self):
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
    def test_logoff_by_number(self):
        app = Mock()
        cmd = LogoffCommand(app, None)
        parsed_args = Namespace(agent_number='1001')
        cmd.take_action(parsed_args)
        app.client.agents.logoff_agent_by_number.assert_called_once_with('1001')

    def test_logoff_all(self):
        app = Mock()
        cmd = LogoffCommand(app, None)
        parsed_args = Namespace(agent_number='all')
        cmd.take_action(parsed_args)
        app.client.agents.logoff_all_agents.assert_called_once()


class TestRelogAllCommand:
    def test_with_timeout(self):
        app = Mock()
        cmd = RelogAllCommand(app, None)
        parsed_args = Namespace(timeout=30)
        cmd.take_action(parsed_args)
        app.client.agents.relog_all_agents.assert_called_once_with(
            recurse=True, timeout=30
        )

    def test_without_timeout(self):
        app = Mock()
        cmd = RelogAllCommand(app, None)
        parsed_args = Namespace(timeout=None)
        cmd.take_action(parsed_args)
        app.client.agents.relog_all_agents.assert_called_once_with(
            recurse=True, timeout=None
        )


class TestStatusCommand:
    def test_single_agent(self):
        app = Mock()
        cmd = StatusCommand(app, None)
        parsed_args = Namespace(agent_number='1001')
        cmd.take_action(parsed_args)
        app.client.agents.get_agent_status_by_number.assert_called_once_with('1001')

    def test_all_agents(self):
        app = Mock()
        app.client.agents.get_agent_statuses.return_value = []
        cmd = StatusCommand(app, None)
        parsed_args = Namespace(agent_number=None)
        cmd.take_action(parsed_args)
        app.client.agents.get_agent_statuses.assert_called_once_with(recurse=True)
