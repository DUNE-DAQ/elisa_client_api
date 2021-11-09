#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Logbook message insert
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : messageInsert.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 27/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : MessageInsert
# Description   : Class providing accessors for the insert operation.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 27/Nov/2012: created.
#--------------------------------------------------------------------------------------

from .messageReply import MessageReply
from .message import Message


class MessageInsert(MessageReply):
    """ Class providing accessors for the insert operation.
    """

    def __init__(self):
        super(MessageInsert, self).__init__(None) 
        
    # --------------------
    # - Property methods -
    # --------------------
    @Message.type.setter
    def type(self, value):
        self._message_type.value = value
