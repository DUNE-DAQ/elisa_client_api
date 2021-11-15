#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Binary to retrieve messages from Elisa.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_get.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 14/Jan/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         :
# Description   : Command line utility to retrieve messages based on an ID
#                 or search criteria from the Elisa back-end.
#--------------------------------------------------------------------------------------
# Copyright (c) 2013 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 14/Jan/2013: created.
# 04/Feb/2013: attachmentsDst instead of attachPath.
#--------------------------------------------------------------------------------------

import logging

from elisa_client_api.exception import *
from elisa_client_api.elisa import Elisa
import elisa_utilhelper as euh


__elisaUtilName__ = 'elisa_get'
__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__)
__author__ = 'Raul Murillo Garcia <rmurillo@cern.ch>'


def writeAttachments(elisa, message, path):
    try:
        attachments = elisa.getAttachments(message)
        for attachment in attachments:
            filename = path + attachment[1]
            with open(filename, "w") as outfile:
                outfile.write(attachment[2])
                logger.debug('Attachment ' + attachment[1] + ' stored in ' + path)

    except IOError as ex:
        logger.error(str(ex))
    except ElisaError as ex:
        logger.error(str(ex))



def main():
    # Command line arguments
    availableArgs = ['version', 'verbosity', 'server', 'sso',
                    'ldap', 'logbook', 'id', 'username','author', 'subject',
                    'type', 'systems', 'options', 'body',
                    'status', 'since', 'to',  'attributes',
                    'interval', 'limit', 'attachmentsDst']
    mandatoryArgs = []
    parser, cmdlArgs = euh.buildCommandLineArguments(__elisaUtilName__, availableArgs, mandatoryArgs)

    if True == cmdlArgs.version:
        print('\n' + __elisaUtilName__ + ' ' +  __version__ + ' (' + __author__ + ')\n')
        sys.exit()

    # Configure the logging module
    logger = logging.getLogger('elisa_get_logger')
    logging.basicConfig(format='%(asctime)s %(funcName)s:%(levelno)s [%(levelname)s]: %(message)s')
    logger.setLevel(euh.getLoggingLevel(cmdlArgs.verbosity))

    # Make sure the interval argument is correctly entered
    # At the moment only months are accepted so the format
    # should be NNm
    interval = cmdlArgs.interval[:-1] if cmdlArgs.interval else None
    if interval != None:
        if not interval.isdigit():
            parser.error("invalid value format of option --interval")
            sys.exit()

    logbook = cmdlArgs.logbook

    elisaArgs = dict()
    elisaArgs['connection'] = euh.getElisaServer(cmdlArgs.server) + euh.getElisaURL() + logbook + '/'
    elisaArgs.update(euh.parseCredentials(cmdlArgs))
    elisa = Elisa(**elisaArgs)

    if None != cmdlArgs.id:
        try:
            message = elisa.getMessage(cmdlArgs.id)
            print(message)
            if None != cmdlArgs.attachmentsDst and 0 != message.hasAttachments:
                writeAttachments(elisa, message, cmdlArgs.attachmentsDst)
        except ElisaError as ex:
            logger.error(str(ex))
    else:
        from searchCriteria import SearchCriteria
        criteria = SearchCriteria()
        criteria.userName = cmdlArgs.username
        criteria.author = cmdlArgs.author
        criteria.subject = cmdlArgs.subject
        criteria.type = cmdlArgs.type
        criteria.systemsAffected = cmdlArgs.systems
        criteria.options = cmdlArgs.options
        criteria.body = cmdlArgs.body
        criteria.status = cmdlArgs.status
        criteria.since = cmdlArgs.since
        criteria.until = cmdlArgs.to
        criteria.interval = interval
        criteria.limit = cmdlArgs.limit

        logger.debug("Search criteria:\n" + str(criteria))

        try:
            messages = elisa.searchMessages(criteria, cmdlArgs.attributes)
            # Dump all the messages and retrieve the attachments if need be.
            for message in messages:
                print(message)
                # Any attachments to be saved?
                if None != cmdlArgs.attachmentsDst and 0 != message.hasAttachments:
                    writeAttachments(elisa, message, cmdlArgs.attachmentsDst)
        except ElisaError as ex:
            logger.error(str(ex))

if __name__ == '__main__':
    main()
