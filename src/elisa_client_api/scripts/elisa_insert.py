#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Binary to insert an elog messages to Elisa.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_insert.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 21/Jan/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         :
# Description   : Command line utility to insert an elog message to the Elisa
#                 back-end database.
#--------------------------------------------------------------------------------------
# Copyright (c) 2013 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 21/Jan/2013: created.
#--------------------------------------------------------------------------------------

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
import logging

from elisa_client_api.exception import *
from elisa_client_api.elisa import Elisa
from elisa_client_api.messageInsert import MessageInsert
import elisa_client_api.scripts.elisa_utilhelper as euh


__elisaUtilName__ = 'elisa_insert'
__version_info__ = ('1', '0', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Raul Murillo Garcia <rmurillo@cern.ch>'


def main():
    # Command line arguments
    availableArgs = ['version', 'verbosity', 'server', 'sso',
                    'ldap', 'logbook', 'author', 'subject', 'type',
                    'systems', 'options', 'body', 'bodyFile',
                    'status', 'attachmentsSrc']
    mandatoryArgs = ['subject', 'type', 'systems']
    parser, cmdlArgs = euh.buildCommandLineArguments(__elisaUtilName__, availableArgs, mandatoryArgs)

    if True == cmdlArgs.version:
        print('\n' + __elisaUtilName__ + ' ' +  __version__ + ' (' + __author__ + ')\n')
        sys.exit()

    # Configure the logging module
    logger = logging.getLogger('elisa')
    logging.basicConfig(format='%(asctime)s %(funcName)s:%(levelno)s [%(levelname)s]: %(message)s')
    logger.setLevel(euh.getLoggingLevel(cmdlArgs.verbosity))

    # Body text can only come from one source
    if cmdlArgs.body and cmdlArgs.bodyFile:
        parser.error('--body and --body-file are mutually exclusive')
        sys.exit()

    msgBody = cmdlArgs.body
    if None != cmdlArgs.bodyFile:
        with open(cmdlArgs.bodyFile) as f:
            msgBody = f.read()

    logbook = cmdlArgs.logbook
    if None == logbook:
        logbook = "ATLAS"

    elisaArgs = dict()
    elisaArgs['connection'] = euh.getElisaServer(cmdlArgs.server) + euh.getElisaURL() + logbook + '/'
    elisaArgs.update(euh.parseCredentials(cmdlArgs))
    elisa = Elisa(**elisaArgs)

    message = MessageInsert()
    message.author = cmdlArgs.author
    message.subject = cmdlArgs.subject
    message.type = cmdlArgs.type
    message.systemsAffected = [sys.strip() for sys in cmdlArgs.systems.split(',')]
    message.options = euh.parseOptions(cmdlArgs.options, parser)
    message.body = msgBody
    message.status = cmdlArgs.status
    message.attachments = cmdlArgs.attachmentsSrc
    logger.debug('\n' + str(message))
    try:
        msgRead = elisa.insertMessage(message)
        logger.debug('\n' + str(msgRead))
    except ElisaError as ex:
        logger.error(str(ex))


