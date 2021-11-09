#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Search criteria
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : searchCriteria.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 22/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : SearchCriteria
# Description   : Class encapsulating all the functionality required to build a search
#                 criteria to retrieve logbook entries from the ELisA database.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 22/Nov/2012: created.
# 04/Dec/2012: use properties.
#--------------------------------------------------------------------------------------

from __future__ import absolute_import
from builtins import str
from builtins import object
from elisa_client_api.core.searchField import SearchField


class SearchCriteria(object):
    """ Class representing a search criteria.
    
    This class provides all the fields required to form a search criteria
    to retrieve logbook messages from the ELisA database.
    """
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self):                
        # -------------------
        # - Data attributes -
        # -------------------
        #  The field name parameter is the same as those use in the ELisA server. 
        #  This schema allows for generic code when serializing, deserializing 
        #  and printing the fields. 
        self._limit = SearchField('limit')          # Number of entries returned (100 by default).
        self._page = SearchField('page')            # Page number for results pagination.
        self._userName = SearchField('userName')    # Filter results per user name.
        self._author = SearchField('author')        # Filter results per author.
        self._systemsAffected = SearchField('systems_affected') # List of system affected to filter entries on.
        self._type = SearchField('message_type')    # Filter per message type.
        self._options = SearchField('options')      # Filter per message options.
        self._subject = SearchField('subject')      # Filter results by subject.
        self._status = SearchField('status')        # Filter results by status.
        self._body = SearchField('body')            # Filter results by body.
        self._since = SearchField('from')           # Initial search date.
        self._until = SearchField('to')             # End search date.
        self._interval = SearchField('month_interval') # Month interval.
    
    
    def __str__(self):
        dump = ""
        fields = self._getFieldNames()
        for field in fields:
            dump += str(getattr(self, field)) + '\n'        
        return dump
    
    
    def getDict(self):
        """ Returns a dictionary of fieldName:fieldValue
        """
        params = {}
        for field in self._getFieldNames():
            attr = getattr(self, field)
            if attr.value != None:
                params[attr.name] = str(attr.value)
        return params
        

    # -------------------------
    # - Public helper methods -
    # -------------------------
    @property
    def limit(self):
        """ Number of entries returned (100 by default). """
        return self._limit.value
    @limit.setter
    def limit(self, value):
        self._limit.value = value
        
    @property
    def page(self):
        """ Page number for results pagination. """
        return self._page.value
    @page.setter
    def page(self, value):
        self._page.value = value
    
    @property
    def userName(self):
        """ Filter results per user name. """
        return self._userName.value
    @userName.setter
    def userName(self, value):
        self._userName.value = value
        
    @property
    def author(self):
        """ Filter results per author. """
        return self._author.value
    @author.setter
    def author(self, value):
        self._author.value = value

    @property
    def systemsAffected(self):
        """ Filter results per systems affected. """
        return self._systemsAffected.value
    @systemsAffected.setter
    def systemsAffected(self, value):
        self._systemsAffected.value = value
        
    @property
    def type(self):
        """ Filter results per type. """
        return self._type.value
    @type.setter
    def type(self, value):
        self._type.value = value
                
    @property
    def options(self):
        """ Filter results per options. """
        return self._options.value
    @options.setter
    def options(self, value):
        self._options.value = value
                    
    @property
    def since(self):
        """ Initial search date. """
        return self._since.value
    @since.setter
    def since(self, value):
        self._since.value = value

    @property
    def until(self):
        """ End search date. """
        return self._until.value
    @until.setter
    def until(self, value):
        self._until.value = value
        
    @property
    def interval(self):
        """ Month interval. """
        return self._interval.value
    @interval.setter
    def interval(self, value):
        self._interval.value = value

    @property
    def subject(self):
        """ Filter results per subject. """
        return self._subject.value
    @subject.setter
    def subject(self, value):
        self._subject.value = value
        
    @property
    def status(self):
        """ Filter results per status. """
        return self._status.value
    @status.setter
    def status(self, value):
        self._status.value = value

    @property
    def body(self):
        """ Filter results per body. """
        return self._body.value
    @body.setter
    def body(self, value):
        self._body.value = value
        
    # -------------------
    # - Private methods -
    # -------------------
    def _getFieldNames(self):
        return [attr for attr in dir(self) if getattr(self, attr).__class__.__name__ == "SearchField"]
        
        
