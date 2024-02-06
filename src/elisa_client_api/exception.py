#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Elisa exceptions
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : exception.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 4/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : ElisaError, ArgumentError
# Description   : Class encapsulating errors that might be raised.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 04/Dec/2012: created.
# 18/Mar/2013: parse the Rest Server error.
#--------------------------------------------------------------------------------------

from builtins import str
import sys


class ElisaError(Exception):
    """ Base exception.
    """
    def __init__(self, reason):
        # Parse REST server errors encapsulated in XML.
        # Format:
        # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        #   <error_report>
        #      <error>
        #        <entry key="status">NOT_FOUND</entry>
        #        <entry key="code">int</entry>
        #        <entry key="message">txt</entry>
        #        <entry key="developerMessage">txt</entry>
        #        <entry key="moreInfoUrl">mailto:luca.magnoni@cern.ch</entry>
        #      </error>
        #   </error_report>
        start = reason.find("<?xml version=")
        end = reason.find("</error_report>")
        if -1 != start and -1 != end:
           import xml.etree.ElementTree as ET
           self.__reason = reason[ : start]
           restSrvError = reason[start : (end + len("</error_report>"))]
           root = ET.fromstring(restSrvError)
           for errors in root.findall('error'):
              entries = errors.findall('entry')
              for entry in entries:
                 self.__reason += '[' + entry.attrib['key'] + ']->' + entry.text
                 if entry != entries[-1]:
                    self.__reason += ', '
        else:
           self.__reason  = reason

        frame = sys._getframe(3)
        self.__operation = frame.f_code.co_filename + "[" + frame.f_code.co_name + "():" + str(frame.f_lineno) + ']'


    def __str__(self):
        return "Exception raised at " + self.__operation + ". Reason: " + self.__reason + "."


class RestServerError(ElisaError):
    """ Exception thrown when an error occurs whilst accessing the rest server.
    """
    def __init__(self, reason):
        super(RestServerError, self).__init__("access to the REST server failed. {0}".format(reason))


class ArgumentError(ElisaError):
    """ Exception thrown when an argument is wrongly passed to the API
    """
    def __init__(self, argument):
        super(ArgumentError, self).__init__("wrong argument. {0}".format(argument))


class FileError(ElisaError):
    """ Elisa exception thrown when an argument is wrongly passed to the API
    """
    pass

