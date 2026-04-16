#!/usr/bin/env python3
# Copyright 2015-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from setuptools import find_packages, setup

setup(
    name='wazo-agentd-cli',
    version='1.0',
    description='a CLI program to interact with a wazo-agentd server',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wazo-agentd-cli = wazo_agentd_cli.main:main',
        ],
        'cliff.formatter.list': [
            'legacy = wazo_agentd_cli.formatters:LegacyAgentStatusFormatter',
        ],
        'wazo_agentd_cli.commands': [
            'add = wazo_agentd_cli.commands:AddAgentToQueueCommand',
            'remove = wazo_agentd_cli.commands:RemoveAgentFromQueueCommand',
            'login = wazo_agentd_cli.commands:LoginCommand',
            'logoff = wazo_agentd_cli.commands:LogoffCommand',
            'relog_all = wazo_agentd_cli.commands:RelogAllCommand',
            'pause = wazo_agentd_cli.commands:PauseCommand',
            'unpause = wazo_agentd_cli.commands:UnpauseCommand',
            'queue_login = wazo_agentd_cli.commands:QueueLoginCommand',
            'queue_logoff = wazo_agentd_cli.commands:QueueLogoffCommand',
            'status = wazo_agentd_cli.commands:StatusCommand',
        ],
    },
)
