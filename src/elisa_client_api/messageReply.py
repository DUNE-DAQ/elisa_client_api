#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Logbook message reply
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : messageReply.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 27/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : MessageReply
# Description   : Class providing accessors for the reply operation.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 27/Nov/2012: created.
#--------------------------------------------------------------------------------------

from __future__ import absolute_import
from elisa_client_api.messageUpdate import MessageUpdate
from elisa_client_api.core.message import Message


class MessageReply(MessageUpdate):
    """ Class providing accessors for the reply operation.
    """

    def __init__(self, msgId=None):
        super(MessageReply, self).__init__(msgId)

    # --------------------
    # - Property methods -
    # --------------------
    @Message.options.setter
    def options(self, value):
        self._options.value = value

    @Message.status.setter
    def status(self, value):
        self._status.value = value

    @Message.author.setter
    def author(self, value):
        self._author.value = value

    @Message.systemsAffected.setter
    def systemsAffected(self, value):
        self._systems_affected.value = value

    @Message.subject.setter
    def subject(self, value):
        self._subject.value = value
