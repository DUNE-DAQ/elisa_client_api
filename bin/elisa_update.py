#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Binary to update an elog messages to Elisa.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_update.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 24/Jan/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : 
# Description   : Command line utility to update an elog message to the Elisa  
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
from elisa_client_api.messageUpdate import MessageUpdate
import elisa_utilhelper as euh


__elisaUtilName__ = 'elisa_update'
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = 'Raul Murillo Garcia <rmurillo@cern.ch>'
    

if __name__ == '__main__':
    # Command line arguments
    availableArgs = ['version', 'verbosity', 'server', 'sso',
                    'ldap', 'logbook', 'id', 'date', 'body', 'bodyFile', 
                    'attachmentsSrc']
    mandatoryArgs = ['id']
    parser, cmdlArgs = euh.buildCommandLineArguments(__elisaUtilName__, availableArgs, mandatoryArgs)

    if True == cmdlArgs.version:
        print('\n' + __elisaUtilName__ + ' ' +  __version__ + ' (' + __author__ + ')\n')
        sys.exit()

    # Configure the logging module
    logger = logging.getLogger('elisa_get_logger')
    logging.basicConfig(format='%(asctime)s %(funcName)s:%(levelno)s [%(levelname)s]: %(message)s')
    logger.setLevel(euh.getLoggingLevel(cmdlArgs.verbosity))
    
    # Make sure at least one option is defined
    if not cmdlArgs.body and not cmdlArgs.attachmentsSrc and not cmdlArgs.bodyFile and not cmdlArgs.date:
        parser.error('why update an e-log without content?')
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
    if None == logbook:
        logbook = "ATLAS"

    elisaArgs = dict()
    elisaArgs['connection'] = euh.getElisaServer(cmdlArgs.server) + euh.getElisaURL() + logbook + '/'
    elisaArgs.update(euh.parseCredentials(cmdlArgs))
    elisa = Elisa(**elisaArgs)
    
    message = MessageUpdate(str(cmdlArgs.id))
    message.body = msgBody
    message.attachments = cmdlArgs.attachmentsSrc
    message.date=cmdlArgs.date
    logger.debug('\n' + str(message)) 
    try:
        msgRead = elisa.updateMessage(message)
        logger.debug('\n' + str(msgRead))
    except ElisaError as ex:
        logger.error(str(ex))


