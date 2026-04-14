# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from cliff.formatters.base import ListFormatter


class LegacyAgentStatusFormatter(ListFormatter):
    def add_argument_group(self, parser):
        pass

    def add_rows(self, data):
        self._rows = data

    def emit_list(self, column_names, data, stdout, parsed_args):
        indices = {name: i for i, name in enumerate(column_names)}
        for row in data:
            row = tuple(row)
            number = row[indices['Number']]
            agent_id = row[indices['ID']]
            logged = row[indices['Logged']]
            stdout.write(f'Agent/{number} (ID {agent_id})\n')
            stdout.write(f'    logged: {logged}\n')
            if logged:
                stdout.write(f'    extension: {row[indices["Extension"]]}\n')
                stdout.write(f'    context: {row[indices["Context"]]}\n')
                stdout.write(
                    f'    state interface: {row[indices["State Interface"]]}\n'
                )
