# Copyright 2015-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_file, read_config_file_hierarchy

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-agentd-cli/config.yml',
    'extra_config_files': '/etc/wazo-agentd-cli/conf.d',
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/wazo-auth-keys/wazo-agentd-cli-key.yml',
    },
    'agentd': {
        'host': 'localhost',
        'port': 9493,
        'prefix': None,
        'https': False,
    },
}


def _args_to_dict(parsed_args):
    agentd_config = {}
    host = getattr(parsed_args, 'host', None)
    if host:
        agentd_config['host'] = host
    port = getattr(parsed_args, 'port', None)
    if port:
        agentd_config['port'] = port

    config = {}
    if agentd_config:
        config['agentd'] = agentd_config

    config_file = getattr(parsed_args, 'config_file', None)
    if config_file:
        config['config_file'] = config_file

    return config


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'service_id': key_file['service_id'],
            'service_key': key_file['service_key'],
        }
    }


def build(parsed_args):
    cli_config = _args_to_dict(parsed_args)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    key_config = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(cli_config, key_config, file_config, _DEFAULT_CONFIG)
