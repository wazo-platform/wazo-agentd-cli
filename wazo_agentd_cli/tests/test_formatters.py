# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from io import StringIO

from wazo_agentd_cli.formatters import LegacyAgentStatusFormatter

COLUMNS = ('number', 'id', 'logged', 'extension', 'context', 'state_interface')


class TestLegacyAgentStatusFormatter:
    def test_logged_agent(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        data = [('1001', 42, True, '1001', 'default', 'SIP/abc')]
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
        data = [('1002', 43, False, '', '', '')]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        assert stdout.getvalue() == ('Agent/1002 (ID 43)\n' '    logged: False\n')

    def test_multiple_agents(self) -> None:
        formatter = LegacyAgentStatusFormatter()
        data = [
            ('1001', 42, True, '1001', 'default', 'SIP/abc'),
            ('1002', 43, False, '', '', ''),
        ]
        stdout = StringIO()

        formatter.emit_list(COLUMNS, data, stdout, parsed_args=None)

        output = stdout.getvalue()
        assert 'Agent/1001 (ID 42)' in output
        assert 'Agent/1002 (ID 43)' in output
        assert output.count('logged:') == 2
