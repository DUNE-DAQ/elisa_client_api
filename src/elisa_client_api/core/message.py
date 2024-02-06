#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Logbook message
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : message.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 27/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : Message
# Description   : Class encapsulating all the fields that describe a logbook message.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 05/Dec/2012: created.
#--------------------------------------------------------------------------------------

from __future__ import absolute_import
from builtins import str
from builtins import object
import string

from .messageField import SimpleField, AttachmentField, SystemsAffectedField, OptionField

class Status(object):
    """ Helper class to specify the status field.
    """
    OPEN = 'open'
    CLOSED = 'closed'


class Message(object):
    """ Class with all the fields of a logbook message.

    Accessors will be provided as needed in derived classes.
    """
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, id):
        # ---------------------------
        # - Private data attributes -
        # ---------------------------

        #  The field name parameter is the same as those use in the ELisA server.
        #  This schema allows for generic code when serializing, deserializing
        #  and printing the fields.
        self._id = SimpleField('id', id)
        self._logbook = SimpleField('logbook')
        self._username = SimpleField('username')
        self._author = SimpleField('author')
        self._date = SimpleField('date')
        self._subject = SimpleField('subject')
        self._message_type = SimpleField('message_type')
        self._systems_affected = SystemsAffectedField('systems_affected')
        self._options = OptionField('options')
        self._body = SimpleField('body')
        self._host = SimpleField('host')
        self._has_replies = SimpleField('has_replies')
        self._reply_to = SimpleField('reply_to')
        self._has_attachments = SimpleField('has_attachments')
        self._attachments = AttachmentField('attachments')
        self._status = SimpleField('status')
        self._thread_head = SimpleField('thread_head')
        self._valid = SimpleField('valid')
        self._encoding = SimpleField('encoding')


    def __str__(self):
        dump = ""
        fields = self.getFieldNames()
        for field in fields:
            dump += str(getattr(self, field)) + '\n'
        return dump


    def getFieldNames(self):
        return [attr for attr in dir(self) if getattr(self, attr).__class__.__name__ == "SimpleField" \
                                           or getattr(self, attr).__class__.__name__ == "AttachmentField" \
                                           or getattr(self, attr).__class__.__name__ == "OptionField" \
                                           or getattr(self, attr).__class__.__name__ == "SystemsAffectedField"]


    def getTag(self):
        return "_"


    # --------------------
    # - Property methods -
    # --------------------
    @property
    def id(self):
        """ Message ID field. """
        return self._id.value

    @property
    def logbook(self):
        """ Message logbook field. """
        return self._logbook.value

    @property
    def userName(self):
        """ Message user name field. """
        return self._username.value

    @property
    def author(self):
        """ Message author field. """
        return self._author.value

    @property
    def date(self):
        """ Message date field. """
        return self._date.value

    @property
    def subject(self):
        """ Message subject field. """
        return self._subject.value

    @property
    def type(self):
        """ Message type field. """
        return self._message_type.value

    @property
    def options(self):
        """ Message options field. """
        return self._options .value

    @property
    def systemsAffected(self):
        """ Message systems affected field. """
        return self._systems_affected.value

    @property
    def body(self):
        """ Message body field. """
        return self._body.value

    @property
    def host(self):
        """ Message host field. """
        return self._host.value

    @property
    def hasReplies(self):
        """ Message has replies field. """
        return self._has_replies.value

    @property
    def replyTo(self):
        """ Message reply to field. """
        return self._reply_to.value

    @property
    def hasAttachments(self):
        """ Message has attachments field. """
        return self._has_attachments.value

    @property
    def attachments(self):
        """ Message attachments field. """
        return self._attachments.value

    @property
    def status(self):
        """ Message status field. """
        return self._status.value

    @property
    def threadHead(self):
        """ Message thread head field. """
        return self._thread_head.value

    @property
    def valid(self):
        """ Message valid field. """
        return self._valid.value

    @property
    def encoding(self):
        """ Message encoding field. """
        return self._encoding.value

