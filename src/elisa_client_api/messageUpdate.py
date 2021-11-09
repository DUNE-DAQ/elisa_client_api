#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Logbook message update
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : messageUpdate.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 27/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : MessageUpdate
# Description   : Class providing accessors for the update operation.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 27/Nov/2012: created.
#--------------------------------------------------------------------------------------

from .messageRead import MessageRead
from .message import Message


class MessageUpdate(MessageRead):
    """ Class providing accessors for the update operation.
    """
    
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, msgId):
        super(MessageUpdate, self).__init__(msgId)
       
    # --------------------
    # - Property methods -
    # --------------------
    @Message.body.setter
    def body(self, value):
        self._body.value = value
            
    @Message.attachments.setter
    def attachments(self, value):
        self._attachments.value = value
        
    @Message.date.setter
    def date(self, value):
        self._date.value = value

