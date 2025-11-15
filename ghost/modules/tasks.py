# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__class_name__="Tasks"

from ghost.ghostlib.GhostModule import GhostArgumentParser, GhostModule, config
from ghost.ghostlib.GhostOutput import Table, Color
from ghost.ghostlib.utils.rpyc_utils import obtain

@config(cat='manage')
class Tasks(GhostModule):
    ''' Get info about registered background tasks '''

    dependencies = ['tasks']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog='tasks', description=cls.__doc__)

    def run(self, args):
        agent = self.client.remote('ghost.agent')
        active = obtain(agent.manager.status)
        data = []
        for task, state in active.items():
            color = 'grey'
            if state['active']:
                color = 'lightgreen'
            elif state['results']:
                color = 'cyan'

            data.append({
                'TASK': Color(task, color),
                'ACTIVE': Color('Y' if state['active'] else 'N', color),
                'RESULTS': Color('Y' if state['results'] else 'N', color),
            })

        self.log(Table(data, ['TASK', 'ACTIVE', 'RESULTS']))
