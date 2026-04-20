# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from io import StringIO
from typing import Any

from wazo_agentd_cli.formatters import LegacyAgentStatusFormatter

COLUMNS = (
    'number',
    'id',
    'logged',
    'extension',
    'context',
    'state_interface',
    'queues',
)


class TestLegacyAgentStatusFormatter:
    def test_logged_agent(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        data: list[tuple[Any, ...]] = [
            ('1001', 42, True, '1001', 'default', 'SIP/abc', [])
        ]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        assert stdout.getvalue() == (
            'Agent/1001 (ID 42)\n'
            '    logged: True\n'
            '    extension: 1001\n'
            '    context: default\n'
            '    state interface: SIP/abc\n'
        )

    def test_not_logged_agent(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        data: list[tuple[Any, ...]] = [('1002', 43, False, '', '', '', [])]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        assert stdout.getvalue() == ('Agent/1002 (ID 43)\n' '    logged: False\n')

    def test_agent_with_queues(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        queues = [
            {'id': 1, 'name': 'support', 'logged': True, 'paused': False},
            {
                'id': 2,
                'name': 'sales',
                'logged': True,
                'paused': True,
                'paused_reason': 'lunch',
            },
        ]
        data: list[tuple[Any, ...]] = [
            ('1001', 42, True, '1001', 'default', 'SIP/abc', queues)
        ]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        assert stdout.getvalue() == (
            'Agent/1001 (ID 42)\n'
            '    logged: True\n'
            '    extension: 1001\n'
            '    context: default\n'
            '    state interface: SIP/abc\n'
            '    queues:\n'
            '        support (ID 1, logged: True)\n'
            '        sales (ID 2, logged: True, paused: lunch)\n'
        )

    def test_agent_with_paused_queue_no_reason(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        queues = [{'id': 1, 'name': 'support', 'logged': True, 'paused': True}]
        data: list[tuple[Any, ...]] = [
            ('1001', 42, True, '1001', 'default', 'SIP/abc', queues)
        ]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        output = stdout.getvalue()
        assert '        support (ID 1, logged: True, paused)\n' in output

    def test_multiple_agents(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        data: list[tuple[Any, ...]] = [
            ('1001', 42, True, '1001', 'default', 'SIP/abc', []),
            ('1002', 43, False, '', '', '', []),
        ]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        output = stdout.getvalue()
        assert 'Agent/1001 (ID 42)' in output
        assert 'Agent/1002 (ID 43)' in output
        assert output.count('logged:') == 2
