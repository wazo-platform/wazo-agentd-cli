# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import Namespace

from wazo_agentd_cli.config import _args_to_dict


class TestArgsToDict:
    def test_no_args(self) -> None:
        parsed_args = Namespace(host=None, port=None, config_file=None)
        result = _args_to_dict(parsed_args)
        assert result == {}

    def test_host_only(self) -> None:
        parsed_args = Namespace(host='myhost', port=None, config_file=None)
        result = _args_to_dict(parsed_args)
        assert result == {'agentd': {'host': 'myhost'}}

    def test_port_only(self) -> None:
        parsed_args = Namespace(host=None, port=9999, config_file=None)
        result = _args_to_dict(parsed_args)
        assert result == {'agentd': {'port': 9999}}

    def test_host_and_port(self) -> None:
        parsed_args = Namespace(host='myhost', port=9999, config_file=None)
        result = _args_to_dict(parsed_args)
        assert result == {'agentd': {'host': 'myhost', 'port': 9999}}

    def test_config_file_only(self) -> None:
        parsed_args = Namespace(host=None, port=None, config_file='/some/path')
        result = _args_to_dict(parsed_args)
        assert result == {'config_file': '/some/path'}

    def test_all_args(self) -> None:
        parsed_args = Namespace(host='myhost', port=9999, config_file='/some/path')
        result = _args_to_dict(parsed_args)
        assert result == {
            'agentd': {'host': 'myhost', 'port': 9999},
            'config_file': '/some/path',
        }
