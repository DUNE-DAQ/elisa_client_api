#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Logbook message read
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : messageRead.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 27/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : MessageRead
# Description   : Class providing accessors for the read operation.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 27/Nov/2012: created.
#--------------------------------------------------------------------------------------

from __future__ import absolute_import
from elisa_client_api.core.message import Message


class MessageRead(Message):
    """ Class providing accessors for the read operation.
    """
    # All the accesssors are getters and are already defined in Message
    def __init__(self, msgId = None):
        super(MessageRead, self).__init__(msgId)
