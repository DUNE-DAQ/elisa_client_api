#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Search criteria field
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : searchField.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 07/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : SearchField
# Description   : Class providing functionality to define a search criteria field.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 07/Dec/2012: created.
#--------------------------------------------------------------------------------------

from builtins import object
class SearchField(object):
    """ Class providing functionality to define a search criteria field.
    """
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name, value = None):
        # ---------------------------
        # - Private data attributes -
        # ---------------------------
        self.__name = name
        self.__value = value

    def __str__(self):
        return '{0:19}: {1}'.format(self.name, self.value)

    # --------------------
    # - Property methods -
    # --------------------
    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        self.__value = value
