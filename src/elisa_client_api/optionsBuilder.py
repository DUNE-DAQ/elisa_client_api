#!/usr/bin/env tdaq_python
#--------------------------------------------------------------------------------------
# Title         : Logbook message options field builder
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : optionsBuilder.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 13/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : OptionsBuilder
# Description   : Helper to build the options field which can have multiple levels
#                 of nested options. Note the user can directly build the list of
#                 options herself without using this helper class.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 13/Dec/2012: created.
#--------------------------------------------------------------------------------------

from builtins import str
from builtins import object
class OptionsBuilder(object):
    """ Class providing functionality to build the options fields.
    """
    # Format
    #    [ { 'name' : 'option1',
    #        'value' : value1,
    #        'options' : ( { 'name' : 'subOption1', 'value' : "subValue1" },
    #                      { 'name' : 'subOption2', 'value' : "subValue2" }
    #                    )
    #      { 'name' : 'option2',
    #        'value' : 'value2' }
    #   ]
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name = "Root", value = None):
        self.__name = name
        self.__value = value
        self.__innerOptions = list()


    def addOption(self, name, value):
        """ Creates an option, adds it to this option's level and returns it.

        name: name of this option.
        value: value of this option.
        Returns: an object of type Option.
        """
        Option = OptionsBuilder
        option = Option(name, value)
        self.__innerOptions.append(option)
        return option


    def toList(self):
        """ Returns a list of options that can be used to insert a message.

        Returns: a list with the options encapsulated as dictionaries.
        """
        optList = list()
        for option in self.__innerOptions:
            optList.append(option.__toDict())
        return optList


    # -------------------
    # - Private methods -
    # -------------------
    def __toDict(self):
        innerOptsList = list()
        for innerOption in self.__innerOptions:
            innerOptsList.append(innerOption.__toDict())

        optDic = {'name' : self.__name, 'value' : str(self.__value) }
        if len(innerOptsList) > 0:
            optDic['options'] = innerOptsList

        return optDic
