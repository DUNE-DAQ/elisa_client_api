#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Logbook message fields
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : messageField.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 05/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : SimpleField, AttachmentField, SystemsAffectedField, OptionField
# Description   : Classes providing accessors, serializers, and deserializers for the
#                 logbook message.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 05/Dec/2012: created.
# 23/Jan/2013: use UTF8 for the name and value of the message fields.
#--------------------------------------------------------------------------------------

from builtins import str
from past.builtins import basestring
from builtins import object
import xml.etree.ElementTree as ET


class SimpleField(object):
    """ Class providing functionality to define a simple message field.

    Simple message fields are those that only contain the field value
    but no nested fields.

    Assume all fields are string type even those that only have numbers
    """
    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name, value = None):
        self.__name = name.encode('utf-8')
        self.__value = str(value) if value != None else None

    def __str__(self):
        return '{0:19}: {1}'.format(self.name.decode('utf-8'), self.value)

    def serialize(self, parentNode):
        if self.value:
            node = ET.SubElement(parentNode, self.name.decode('utf-8'))
            node.text = str(self.value)

    def deserialize(self, node):
        if node.text != None:
            self.value = node.text.encode('utf-8').decode('utf-8')


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

    # ---------------------------
    # - Private data attributes -
    # ---------------------------
    __name = None
    __value = None


class SystemsAffectedField(object):
    """ Class providing functionality to define the message systems
    affected field.

    This field contains a list with the systems affected names.
    """
    # Format:
    #  <systems_affected>
    #    <count> 2 </count>
    #    <system_affected>DAQ</system_affected>
    #    <system_affected>HLT</system_affected>
    #  </systems_affected>

    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name):
        # ---------------------------
        # - Private data attributes -
        # ---------------------------
        self.__name = name.encode('utf-8')
        self.__value = list()

    def __str__(self):
        return '{0:19}: {1}'.format(self.name.decode('utf-8'), self.value)

    def serialize(self, parentNode):
        if not self.value:
            return

        if len(self.value) > 0:
            rootNode = ET.SubElement(parentNode, self.name.decode('utf-8'))
            countNode = ET.SubElement(rootNode, 'count')
            countNode.text = str(len(self.value))
            for system in self.value:
                sysNode = ET.SubElement(rootNode, 'system_affected')
                sysNode.text = system


    def deserialize(self, node):
        [self.value.append(child.text.encode('utf-8').decode('utf-8')) for child in node.findall('system_affected')]

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


class AttachmentField(object):
    """ Class providing functionality to define the message attachment field.

    This field contains a list of tuples with the following simple fields:
    filename, ID and link
    """
    # Format:
    #  <attachments>
    #    <count>1</count>
    #    <attachment>
    #      <filename>foto.jpg</filename>
    #      <ID>0</ID>
    #      <link>http://example.com/elisa.api/api/messages/200006/attachment/0</link>
    #    </attachment>
    #  </attachments>

    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name):
        # ---------------------------
        # - Private data attributes -
        # ---------------------------
        self.__name = name.encode('utf-8')
        self.__value = None

    def __str__(self):
        if not self.value:
            return '{0:19}: 0'.format(self.name.decode('utf-8'))

        dump = '{0:19}: {1}'.format(self.name.decode('utf-8'), len(self.value))
        # Message insertion encapsulates attachments as a list of strings.
        # Message retrieval encapsulates attachments as a list of tuples.
        if isinstance(self.value[0], basestring):
            for attach in self.value:
                dump += '\n    |---- {0}'.format(attach)
        else:
            for attach in self.value:
                dump += '\n    |---- {0:4}: {1}'.format("ID", attach[0])
                dump += '\n    |---- {0:4}: {1}'.format("Name", attach[1])
                dump += '\n    |---- {0:4}: {1}'.format("Link", attach[2])
        return dump

    def serialize(self, parentNode):
        # Attachments are never serialized because its insertion follows
        # a different path.
        pass

    def deserialize(self, node):
        self.value = list()
        [self.__value.append((child.find('ID').text.encode('utf-8').decode('utf-8'),
                              child.find('filename').text.encode('utf-8').decode('utf-8'),
                              child.find('link').text.encode('utf-8').decode('utf-8')))
         for child in node.findall('attachment')]


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


class OptionField(object):
    """ Class providing functionality to define the message option field.

    This field contains a list of tuples with the following fields:
    name, value, list of OptionField
    """
    # Format:
    #  <options>
    #    <count>1</count>
    #    <option>
    #      <name> Option1 </name>
    #      <value> value </value>
    #      <options>
    #        <count>1</count>
    #        <option>
    #          <name> inner_option1 </name>
    #          <value> value </value>
    #        <option>
    #      <options>
    #    </option>

    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, name):
        # ---------------------------
        # - Private data attributes -
        # ---------------------------
        self.__name = name.encode('utf-8')
        self.__value = list()


    def __str__(self):
        if not self.value:
            return '{0:19}: 0'.format(self.name.decode('utf-8'))

        dump = '{0:19}: {1}'.format(self.name.decode('utf-8'), len(self.value))
        # First level options
        for option in self.value:
            dump += '\n    |---- {0:14}: {1}'.format(option['name'], option['value'])
            # Second level options
            innerOptions = option.get('options', None)
            if innerOptions != None:
                for innerOpt in innerOptions:
                    dump += '\n          |---- {0:14}: {1}'.format(innerOpt['name'], innerOpt['value'])

        return dump


    def serialize(self, parentNode):
        if not self.value:
            return

        count = len(self.value)
        if count == 0:
            return
        # First level
        rootNode = ET.SubElement(parentNode, 'options')
        for option in self.value:
            optionNode = ET.SubElement(rootNode, 'option')
            ET.SubElement(optionNode, 'name').text = str(option['name'])
            ET.SubElement(optionNode, 'value').text = str(option['value'])
            innerOptions = option.get('options', None)
            if innerOptions == None:
                continue
            # Second level options
            optionsNode = ET.SubElement(optionNode, 'options')
            for innerOption in innerOptions:
                innerOptionNode = ET.SubElement(optionsNode, 'option')
                ET.SubElement(innerOptionNode, 'name').text = str(innerOption['name'])
                ET.SubElement(innerOptionNode, 'value').text = str(innerOption['value'])
            ET.SubElement(optionsNode, 'count').text = str(len(innerOptions))

        ET.SubElement(rootNode, 'count').text = str(count)


    def deserialize(self, node):
        optionNodes = node.findall('option')
        # First level options
        for option in optionNodes:
            # Second level options
            listInnerOpts = list()
            [[listInnerOpts.append( { 'name' : innerOptionNodes.find('name').text.encode('utf-8').decode('utf-8'),
                                      'value' : innerOptionNodes.find('value').text.encode('utf-8').decode('utf-8') })
              for innerOptionNodes in innerOptionsNode.findall('option')]
             for innerOptionsNode in option.findall('options')]

            self.value.append({ 'name' : option.find('name').text.encode('utf-8').decode('utf-8'),
                               'value' : option.find('value').text.encode('utf-8').decode('utf-8'),
                               'options' : listInnerOpts })


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


