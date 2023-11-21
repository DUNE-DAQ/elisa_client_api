#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Binary to reply an elog messages to Elisa.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_reply.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 24/Jan/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         :
# Description   : Command line utility to reply an elog message to the Elisa
#                 back-end database.
#--------------------------------------------------------------------------------------
# Copyright (c) 2013 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 24/Jan/2013: created.
#--------------------------------------------------------------------------------------

import logging

from elisa_client_api.exception import *
from elisa_client_api.elisa import Elisa
from elisa_client_api.messageReply import MessageReply
from elisa_client_api.scripts.elisa_utilhelper import *


__elisaUtilName__ = 'elisa_reply'
from elisa_client_api import __version__
__author__ = 'Raul Murillo Garcia <rmurillo@cern.ch> & Pierre Lasorak <pierre.lasorak@cern.ch>'

def main():
    # Command line arguments
    availableArgs = ['version', 'verbosity', 'server', 'sso',
                    'ldap', 'logbook', 'id', 'author', 'systems',
                    'options', 'body', 'bodyFile',
                    'status', 'attachmentsSrc']
    mandatoryArgs = ['id']
    parser, cmdlArgs = buildCommandLineArguments(__elisaUtilName__, availableArgs, mandatoryArgs)

    if True == cmdlArgs.version:
        print('\n' + __elisaUtilName__ + ' ' +  __version__ + ' (' + __author__ + ')\n')
        sys.exit()

    # Configure the logging module
    logger = logging.getLogger('elisa')
    logging.basicConfig(format='%(asctime)s %(funcName)s:%(levelno)s [%(levelname)s]: %(message)s')
    logger.setLevel(getLoggingLevel(cmdlArgs.verbosity))

    # Make sure at least one option is defined
    if not cmdlArgs.author and not cmdlArgs.systems and not cmdlArgs.options and \
       not cmdlArgs.body and not cmdlArgs.bodyFile and not cmdlArgs.attachmentsSrc and \
       not cmdlArgs.status:
        parser.error('why reply with an empty e-log?')
        sys.exit()

    # Body text can only come from one source
    if cmdlArgs.body and cmdlArgs.bodyFile:
        parser.error('--body and --body-file are mutually exclusive')
        sys.exit()

    msgBody = cmdlArgs.body
    if None != cmdlArgs.bodyFile:
        with open(cmdlArgs.bodyFile) as f:
            msgBody = f.read()

    logbook = cmdlArgs.logbook

    elisaArgs = dict()
    elisaArgs['connection'] = getElisaServer(cmdlArgs.server) + getElisaURL() + logbook + '/'
    elisaArgs.update(parseCredentials(cmdlArgs))
    elisa = Elisa(**elisaArgs)

    message = MessageReply(cmdlArgs.id)
    message.author = cmdlArgs.author
    message.systemsAffected = [sys.strip() for sys in cmdlArgs.systems.split(',')] if cmdlArgs.systems else None
    message.options = parseOptions(cmdlArgs.options, parser)
    message.body = msgBody
    message.status = cmdlArgs.status
    message.attachments = cmdlArgs.attachmentsSrc
    logger.debug('\n' + str(message))
    try:
        msgRead = elisa.replyToMessage(message)
        logger.debug('\n' + str(msgRead))
    except ElisaError as ex:
        logger.error(str(ex))


if __name__ == '__main__':
    main()
