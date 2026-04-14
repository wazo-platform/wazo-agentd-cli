# Copyright 2012-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import sys

import wazo_agentd_client
import wazo_auth_client
from cliff.app import App
from cliff.commandmanager import CommandManager

from . import config

logging.getLogger('requests').setLevel(logging.ERROR)


class WazoAgentdCLI(App):
    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super().__init__(
            description='A CLI for the wazo-agentd service',
            command_manager=CommandManager('wazo_agentd_cli.commands'),
            version='0.0.1',
        )
        self._current_token = None
        self._remove_token = False
        self._client = None
        self._auth_client = None

    def build_option_parser(self, *args, **kwargs):
        parser = super().build_option_parser(*args, **kwargs)
        parser.add_argument('--config-file', help='Path to the configuration file')
        parser.add_argument('--host', help='Hostname of the wazo-agentd server')
        parser.add_argument('--port', type=int, help='Port of the wazo-agentd server')
        return parser

    @property
    def client(self):
        if not self._client:
            self._client = wazo_agentd_client.Client(**self._agentd_config)

        if not self._current_token:
            auth_config = dict(self._auth_config)
            username = auth_config.pop('service_id')
            password = auth_config.pop('service_key')
            auth_config.pop('key_file', None)
            self._auth_client = wazo_auth_client.Client(
                username=username, password=password, **auth_config
            )
            token_data = self._auth_client.token.new(expiration=3600)
            self._current_token = token_data['token']
            self._remove_token = True

        self._client.set_token(self._current_token)
        return self._client

    def initialize_app(self, argv):
        self.LOG.debug('Wazo Agentd CLI')
        self.LOG.debug('options=%s', self.options)
        conf = config.build(self.options)
        self.LOG.debug('Starting with config: %s', conf)
        self._auth_config = dict(conf['auth'])
        self._agentd_config = dict(conf['agentd'])

    def clean_up(self, cmd, result, err):
        if err:
            self.LOG.debug('got an error: %s', err)

        if self._remove_token:
            self._auth_client.token.revoke(self._current_token)
            self._current_token = None
            self._remove_token = False


def _expand_deprecated_command_flag(argv):
    """Support legacy -c/--command flag by expanding its value into argv.

    e.g. ['-c', 'login 1001 ext ctx'] -> ['login', '1001', 'ext', 'ctx']
    """
    argv = list(argv)
    for i, arg in enumerate(argv):
        for flag in ('-c', '--command'):
            if arg == flag and i + 1 < len(argv):
                command_str = argv[i + 1]
                argv[i : i + 2] = command_str.split()
            elif arg.startswith(f'{flag}='):
                command_str = arg[len(flag) + 1 :]
                argv[i : i + 1] = command_str.split()
            else:
                continue
            print(
                f'Warning: {flag} is deprecated, use: wazo-agentd-cli {command_str}',
                file=sys.stderr,
            )
            return argv
    return argv


def main(argv=sys.argv[1:]):
    app = WazoAgentdCLI()
    return app.run(_expand_deprecated_command_flag(argv))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
