# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import Mock, patch

from wazo_agentd_cli.main import WazoAgentdCLI, _expand_deprecated_command_flag


class TestExpandCommandFlag:
    def test_no_flag(self) -> None:
        assert _expand_deprecated_command_flag(['status']) == ['status']

    def test_short_flag(self) -> None:
        result = _expand_deprecated_command_flag(['-c', 'login 1001 1001 default'])
        assert result == ['login', '1001', '1001', 'default']

    def test_long_flag(self) -> None:
        result = _expand_deprecated_command_flag(['--command', 'status 1001'])
        assert result == ['status', '1001']

    def test_flag_with_other_args(self) -> None:
        result = _expand_deprecated_command_flag(['--host', 'myhost', '-c', 'status'])
        assert result == ['--host', 'myhost', 'status']

    def test_long_flag_equals_format(self) -> None:
        result = _expand_deprecated_command_flag(['--command=status 1001'])
        assert result == ['status', '1001']

    def test_short_flag_equals_format(self) -> None:
        result = _expand_deprecated_command_flag(['-c=status 1001'])
        assert result == ['status', '1001']

    def test_flag_without_value(self) -> None:
        assert _expand_deprecated_command_flag(['-c']) == ['-c']


class TestClientProperty:
    def _make_app(self) -> WazoAgentdCLI:
        with patch.object(WazoAgentdCLI, '__init__', lambda self: None):
            app = WazoAgentdCLI()
        app._current_token = None
        app._remove_token = False
        app._client = None
        app._auth_client = None
        app._agentd_config = {
            'host': 'localhost',
            'port': 9493,
        }
        app._auth_config = {
            'host': 'localhost',
            'port': 9497,
            'service_id': 'my-service',
            'service_key': 'my-secret',
            'key_file': '/some/path',
        }
        return app

    @patch('wazo_agentd_cli.main.AuthClient')
    @patch('wazo_agentd_cli.main.AgentdClient')
    def test_creates_token_lazily(self, mock_agentd: Mock, mock_auth: Mock) -> None:
        mock_auth.return_value.token.new.return_value = {'token': 'my-token'}
        app = self._make_app()

        client = app.client

        mock_auth.assert_called_once_with(
            username='my-service',
            password='my-secret',
            host='localhost',
            port=9497,
        )
        mock_auth.return_value.token.new.assert_called_once_with(expiration=3600)
        mock_agentd.assert_called_once_with(host='localhost', port=9493)
        client.set_token.assert_called_with('my-token')
        assert app._remove_token is True

    @patch('wazo_agentd_cli.main.AuthClient')
    @patch('wazo_agentd_cli.main.AgentdClient')
    def test_caches_on_second_access(self, mock_agentd: Mock, mock_auth: Mock) -> None:
        mock_auth.return_value.token.new.return_value = {'token': 'my-token'}
        app = self._make_app()

        app.client
        app.client

        mock_auth.return_value.token.new.assert_called_once()


class TestCleanUp:
    def test_revokes_token_when_created(self) -> None:
        app = Mock(spec=WazoAgentdCLI)
        app._remove_token = True
        app._current_token = 'my-token'
        app._auth_client = Mock()

        WazoAgentdCLI.clean_up(app, cmd=None, result=None, err=None)

        app._auth_client.token.revoke.assert_called_once_with('my-token')
        assert app._remove_token is False

    def test_does_nothing_when_no_token(self) -> None:
        app = Mock(spec=WazoAgentdCLI)
        app._remove_token = False
        app._auth_client = Mock()
        app.LOG = Mock()

        WazoAgentdCLI.clean_up(app, cmd=None, result=None, err=None)

        app._auth_client.token.revoke.assert_not_called()
