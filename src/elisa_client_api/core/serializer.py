#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : XML formatter
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : serializer.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 23/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : Serializer
# Description   : Class encapsulating serializing and deserializing methods of the
#                 logbook message.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 23/Nov/2012: created.
# 04/Feb/2013: bug in deserializeMessageTypeOptions()
#--------------------------------------------------------------------------------------

from builtins import object
import xml.etree.ElementTree as ET
import string
import logging
from lxml import etree

from elisa_client_api.messageRead import MessageRead


class FormatterError(Exception):
    """ Formatter exception thrown when an error occurs whilst serializing
    or deserializing XML string.
    """
    def __init__(self, reason):
        self.reason  = reason
    def __str__(self):
        return "XML formatter exception: " + self.reason + "."


class Serializer(object):
    """ Class providing serializing and deserializing methods for the
    logbook message.
    """

    def serialize(self, message, topNodeName):
        """ Creates an XML format string from a logbook message.

        message: the object to serialize.
        Returns: the XML representation of the logbook message.
        Throws: FormatterError if serializing the message fails.
        """
        root = ET.Element(topNodeName)
        fields = message.getFieldNames()
        for field in fields:
            attr = getattr(message, field)
            attr.serialize(root)

        return ET.tostring(root)


    def deserialize(self, xmlStr):
        """ Creates an object of type MessageRead from an XML format string.

        xmlStr: the XML string representation of the logbook message.
        Returns: one object of type MessageRead or a list these objects.
        Throws: FormatterError if deserializing the message fails.
        """
        #print (xmlStr)
        my_parser = etree.XMLParser(recover=True)
        root = ET.fromstring(xmlStr,parser = my_parser)
        # Check if there is one message only or a list of them
        if root.tag == "message":
            # One message
            return self._deserializeMessage(root)
        # Many messages
        listMsgs = list()
        [listMsgs.append(self._deserializeMessage(node)) for node in root.findall('message')]
        return listMsgs


    def deserializeMessageTypes(self, xmlStr):
        """ Creates a list with the message types as defined in the
        ElisA logbook configuration.

        xmlStr: the XML string representation the logbook configuration.
        Returns: a list with the message types.
        Throws: FormatterError if deserializing the types fails.
        """
        types = list()
        root = ET.fromstring(xmlStr)
        for child in root.findall('message_type'):
            types.append(child.text)
        return types


    def deserializeMessageTypeOptions(self, xmlStr):
        """ Creates a dictionary with the options for a given message type.
        as defined in the ElisA logbook configuration.

        xmlStr: the XML string representation the message type options.
        Returns: a dictionary with the option name as key and option
                fields and values ad key/value pairs.
        Throws: FormatterError if deserializing the options fails.
        """
        opts = list()
        rootOption = ET.fromstring(xmlStr)

        # First level options
        for optionNode in rootOption.findall('option'):
            optionVals = dict()
            # Second level options
            listInnerOpts = list()
            for innerOptionsNode in optionNode.findall('options'):
                for innerOptionNode in innerOptionsNode.findall('option'):
                    elemDic = dict()
                    for k in ['name', 'type', 'comment', 'possible_values']:
                        elemDic[k] = innerOptionNode.find(k).text if innerOptionNode.find(k) != None else ""
                    listInnerOpts.append(elemDic)

            # Add first level option
            for k  in ['name', 'type', 'comment', 'possible_values'] :
                optionVals[k] = optionNode.find(k).text if optionNode.find(k) != None else ""

# Valid as of python 2.7
#                    listInnerOpts.append( { k:innerOptionNode.find(k).text
#                                           for k in ['name', 'type', 'comment', 'possible_values']
#                                           if innerOptionNode.find(k) != None } )
            # Add first level option
#            optionVals = { k:optionNode.find(k).text for k  in ['name', 'type', 'comment', 'possible_values']
#                             if optionNode.find(k) != None }
            optionVals['options'] = listInnerOpts if len(listInnerOpts) > 0 else ""
            opts.append(optionVals)

        return opts


    def deserializeSystemsAffected(self, xmlStr):
        """ Creates a list with the systems affected as defined in the
        ElisA logbook configuration.

        xmlStr: the XML string representation the logbook configuration.
        Returns: a list with the systems affected.
        Throws: FormatterError if deserializing the types fails.
        """
        types = list()
        root = ET.fromstring(xmlStr)
        for child in root.findall('system_affected'):
            types.append(child.text)
        return types

    # -------------------
    # - Private methods -
    # -------------------
    def _deserializeMessage(self, node):
        """ Creates an object of type MessageRead from an XML format string.

        node: the XML node representing the logbook message.
        Returns: an object of type MessageRead.
        Throws: TBD
        """
        message = MessageRead()
        for child in node:
            attr = getattr(message, message.getTag() + child.tag)
            if attr != None:
                attr.deserialize(child)
            else:
                logging.error("Unknown XML tag in message: " + child.tag)
        return message
