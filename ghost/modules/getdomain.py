# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__="GetDomain"

@config(compat="windows", cat="admin")
class GetDomain(GhostModule):
    """ Get primary domain controller """

    dependencies = ['pupwinutils.getdomain']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="getdomain", description=cls.__doc__)

    def run(self, args):
        get_domain_controller = self.client.remote('pupwinutils.getdomain', 'get_domain_controller')

        primary_domain = get_domain_controller()
        if not primary_domain:
            self.error("This host is not part of a domain.")
        else:
            self.success("Primary domain controller: %s" % primary_domain)
