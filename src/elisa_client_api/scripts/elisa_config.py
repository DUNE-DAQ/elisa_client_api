#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Binary to retrieve the Elisa configuration.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_config.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 04/Feb/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         :
# Description   : Command line utility to retrieve the Elisa configuration.
#--------------------------------------------------------------------------------------
# Copyright (c) 2013 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 04/Feb/2013: created.
#--------------------------------------------------------------------------------------

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
import logging

from elisa_client_api.exception import *
from elisa_client_api.elisa import Elisa
import elisa_utilhelper as euh


__elisaUtilName__ = 'elisa_config'
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = 'Raul Murillo Garcia <rmurillo@cern.ch>'


if __name__ == '__main__':
    # Command line arguments
    availableOpts = ['version', 'verbosity', 'server', 'sso',
                    'ldap', 'type']
    mandatoryArgs = []
    parser, cmdlArgs = euh.buildCommandLineArguments(__elisaUtilName__, availableOpts, mandatoryArgs)

    if True == cmdlArgs.version:
        print('\n' + __elisaUtilName__ + ' ' +  __version__ + ' (' + __author__ + ')\n')
        sys.exit()

    # Configure the logging module
    logger = logging.getLogger('elisa_get_logger')
    logging.basicConfig(format='%(asctime)s %(funcName)s:%(levelno)s [%(levelname)s]: %(message)s')
    logger.setLevel(euh.getLoggingLevel(cmdlArgs.verbosity))

    elisaArgs = dict()
    elisaArgs['connection'] = euh.getElisaServer(cmdlArgs.server) + euh.getElisaURL()
    elisaArgs.update(euh.parseCredentials(cmdlArgs))
    elisa = Elisa(**elisaArgs)

    try:
        if cmdlArgs.type:
            print("\nValid options for " + cmdlArgs.type + ":")
            listOpts = elisa.getMessageType(cmdlArgs.type)
            # Dump list of options as the user would need to type them in the utilities.
            for opt in listOpts:
                print("  Name:            " + opt['name'])
                print("  Type:            " + opt['type'])
                print("  Possible values: " + opt['possible_values'])
                print("  Comment:         " + opt['comment'])
                print("  Inner options:")
                # Inner options
                for innerOpt in opt['options']:
                    print("      Name:            " + innerOpt['name'])
                    print("      Type:            " + innerOpt['type'])
                    print("      Possible values: " + innerOpt['possible_values'])
                    print("      Comment:         " + innerOpt['comment'])
        else:
            print("\nList of possible types:")
            print(elisa.getMessageType())

        print(("\nValid systems affected for " + cmdlArgs.type + ":") if cmdlArgs.type else "\nList of possible systems affected:")
        print(elisa.getSystemsAffected(cmdlArgs.type))

        print("\n")
    except ElisaError as ex:
        logger.error(str(ex))
