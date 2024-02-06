#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Interface to the ELisA logbook database.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 22/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : Elisa
# Description   : Interface to the ELisA logbook database.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 22/Nov/2012: created.
# 08/Jan/2013: add authentication.
# 11/Feb/2013: add option to show attributes when searching for messages.
#--------------------------------------------------------------------------------------

from __future__ import absolute_import
from builtins import object
from elisa_client_api.core.restServer import RestServer
from elisa_client_api.core.authentication import Authentication


class Elisa(object):
    """ Interface to the ELisA logbook database.
    """
    def __init__(self, connection, username=None, password=None, ssocookie=None):
        """ Constructor

        connection: connection to the logbook database back-end.
        username: user name to be used by ldap.
        password: password to be used with ldap.
        ssocookie: file with the sso-cookie created by auth-get-sso-cookie
        """
        authenticaiton = Authentication(username, password, ssocookie)
        self._server = RestServer(connection, authenticaiton)

    # -----------------------------
    # - Public methods: Interface -
    # -----------------------------
    def getMessage(self, msgId):
        """ Retrieves the logbook message with the given ID.

        This method interacts with the ELisA logbook to retrieve
        the message with the associated ID given in the argument.
        The validity of this criteria is realized at the server side.

        msgId: the message ID.
        Returns: an object of type MessageRead encapsulating the message
                 with the given ID.
        Throws: ElisaError if accessing the logbook fails.
        """
        return self._server.getMessage(msgId)


    def getAttachment(self, msgId, attachmentId):
        """ Retrieves the attachment with the given ID for the given message ID.

        This method interacts with the ELisA logbook to retrieve the
        attachment with the given ID for the given message ID.

        The validity of this criteria is realized at the server side.

        Users are encourage to use getAttachments() since it does
        not imply knowing IDs.

        msgId: message ID of the attachment to retrieve.
        attachmentId: the attachment ID
        Returns: the attachment.
        Throws: ElisaError if accessing the logbook fails.
        """
        return self._server.getAttachment(msgId, attachmentId)


    def getAttachments(self, message):
        """ Retrieves all the attachments for a logbook message.

        This method interacts with the ELisA logbook to retrieve
        all the attachments for the message in the arguments.
        The validity of this criteria is realized at the server side.

        message: object of type MessageRead with the attachment to retrieve.
        Returns: a list of tuples with the id, name and content of the attachments.
        Throws: ElisaError if accessing the logbook fails.
        """
        return self._server.getAttachments(message)


    def searchMessages(self, criteria, showAttributes=False):
        """ Retrieves the logbook messages that match the given search criteria.

        This method interacts with the ELisA logbook to retrieve
        those messages that match the search criteria defined in
        the 'criteria' argument. The validity of this criteria
        is realized at the server side.

        criteria: object of type SearchCriteria specifying the search
                  filter.
        showAttributes: if true, it also returns the option and attachment
                        message fields.
        Returns: a list of objects of type MessageRead encapsulating
                 the messages that meet the search criteria.
        Throws: ElisaError if accessing the logbook fails.
        """
        return self._server.searchMessages(criteria, showAttributes)


    def insertMessage(self, message):
        """ Inserts a logbook message into the ELisA back-end database.

        Inserts in the ELisA logbook back-end database the message encapsulated
        in the 'message' argument. The type of this argument must be MessageWrite.
        The message consistency check is realized at the server side. The expected
        message type

        message: object of type MessageWrite to be inserted into the database.
        Returns: an object of type MessageRead encapsulating the message
                 inserted into the database.
        Throws: ElisaError if accessing the logbook fails.
        """
        return self._server.insertMessage(message)


    def updateMessage(self, message):
        """ Updates a logbook message.

        Inserts the updated message encapsulated in the 'message' argument.
        The type of this argument must be MessageUpdate. The message consistency
        check is realized at the server side.

        message: object of type MessageUpdate to be inserted into the database.
        Returns: an object of type MessageRead encapsulating the message
                 updated into the database.
        Throws: ElisaError if updating the message fails.
        """
        return self._server.updateMessage(message)


    def replyToMessage(self, message):
        """ Replies to a logbook message.

        Inserts the reply message encapsulated in the 'message' argument.
        The type of this argument must be MessageReply. The message consistency
        check is realized at the server side.

        message: object of type MessageReply to be inserted into the
                 database.
        Returns: an object of type MessageRead encapsulating the message
                 inserted into the database.
        Throws: ElisaError if the reply message could not be inserted.
        """
        return self._server.replyToMessage(message)


    def getMessageType(self, msgType=None):
        """ Retrieves the possible message types or the options for
        a message type is specified in the argument.

        msgType: a message type.
        Returns: a list of message types or a dictionary with the options
                 associated to a specific type.
        Throws: ElisaError if accessing the logbook fails.
        """
        if msgType == None:
            return self._server.getMessageTypes()
        else:
            return self._server.getTypeOptions(msgType)


    def getSystemsAffected(self, msgType=None):
        """ Retrieves the possible systems affected or the predefined
        systems affected for a given message type if that type is
        specified in the argument.

        msgType: a message type.
        Returns: a list of possible systems affected or a list of
                 predefined systems affected for a given message type.
        Throws: ElisaError if accessing the logbook fails.
        """
        if msgType == None:
            return self._server.getSystemsAffected()
        else:
            return self._server.getPredefinedSystemsAffected(msgType)


    # ---------------------------
    # - Private data attributes -
    # ---------------------------
    _server = None  # ELisA server.

