#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Unit test for the message serialization.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : serializeTest.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 17/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : SerializeTest
# Description   : Unit test for the message serialization. 
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 17/Dec/2012: created.
#--------------------------------------------------------------------------------------

import unittest
import logging

from serializer import Serializer
from messageInsert import MessageInsert


class SerializeTest(unittest.TestCase):
    """ Test for the message serialization. 
    """
    def setUp(self):
        pass

    
    # -------------------------
    # - Public methods: tests -
    # -------------------------
    def test_serializeMessage(self):
        """ Tests the message serialization functionality.
        """
        logging.debug("Testing the serialization of a message.")
        message = MessageInsert()
        message.author = 'Raul Murillo'
        message.subject = 'Unit test'        
        message.body = 'Test'
        message.type = 'Trigger'        
        message.systemsAffected = ['HLT', 'LVL1']
        message.options = [{'name': 'Trigger_Area', 'value': 'Trigger Group', 'options': []}]
        message.attachments = ['/Users/rmurillo/barcelona.jpg']
        msgXml = Serializer().serialize(message, 'input_message')
        expectedXml = """<input_message><author>Raul Murillo</author><body>Test</body><message_type>Trigger</message_type><options><option><name>Trigger_Area</name><value>Trigger Group</value><options><count>0</count></options></option><count>1</count></options><subject>Unit test</subject><systems_affected><count>2</count><system_affected>HLT</system_affected><system_affected>LVL1</system_affected></systems_affected></input_message>"""
        self.assertEqual(msgXml, expectedXml)


    def test_deserializeMessage(self):
        """ Tests the message deserialization functionality.
        """
        logging.debug("Testing the deserialization of a message.")
        xmlIn = """<message>
        <author>Raul Murillo</author>
        <subject>Unit test</subject>
        <date>2012-12-14T12:27:17+01:00</date>
        <body>Test</body>
        <message_type>Trigger</message_type>
        <systems_affected>
        <count>2</count>
        <system_affected>HLT</system_affected>
        <system_affected>LVL1</system_affected>
        </systems_affected>
        <id>132814</id>
        <logbook>70</logbook>
        <encoding>3</encoding>
        <has_attachments>1</has_attachments>
        <has_replies>0</has_replies>
        <reply_to>0</reply_to>
        <thread_head>132814</thread_head>
        <valid>valid</valid>
        <options>
        <count>1</count>
        <option>
        <name>Trigger_Area</name>
        <value>Trigger Group</value>
        </option>
        </options>
        <attachments>
        <count>1</count>
        <attachment>
        <filename>barcelona.jpg</filename>
        <ID>1239088</ID>
        <link>http://pcatd137.cern.ch:8080/elisa.api/api/messages/132789/attachments/1239088</link>
        </attachment></attachments>
        </message>"""
        message = Serializer().deserialize(xmlIn)
        self.assertEqual(message.author, 'Raul Murillo')
        self.assertEqual(message.subject, 'Unit test')
        self.assertEqual(message.body, 'Test')
        self.assertEqual(message.date, '2012-12-14T12:27:17+01:00')
        self.assertEqual(message.type, 'Trigger')
        self.assertEqual(message.systemsAffected, ['HLT', 'LVL1'])
        self.assertEqual(message.encoding, '3')
        self.assertEqual(message.logbook, '70')
        self.assertEqual(message.hasAttachments, '1')
        self.assertEqual(message.hasReplies, '0')
        self.assertEqual(message.replyTo, '0')
        self.assertEqual(message.threadHead, '132814')
        self.assertEqual(message.valid, 'valid')
        self.assertEqual(message.options, [{'name': 'Trigger_Area', 'value': 'Trigger Group', 'options': []}])
        self.assertEqual(message.attachments, [('1239088', 'barcelona.jpg', 'http://pcatd137.cern.ch:8080/elisa.api/api/messages/132789/attachments/1239088')])
        self.assertEqual(message.id, '132814')
         
 
    def test_serializeConfig(self):
        """ Tests the operation 'search messages'.
        """
        from elisa import Elisa
        from exception import ElisaError
        
        elisa = Elisa("http://pcatd137.cern.ch:8080/elisa.api/api/")
        
        # This might fail if the configuration changes.
        logging.debug("Testing the serialization of the configuration.")
        expectedTypes = ['Default Message Type', 'Shift Summary', 'Shift Leader', 'Run Control', 'Online', 'Trigger', 'LVL1', 'Data Quality', 'Pixel', 'SCT', 'ID General', 'LArg', 'Tile', 'BCM', 'DCS', 'DSS', 'GAS', 'Cooling', 'Slimos-TI', 'Check list']
        types = elisa.getMessageType()
        self.assertEqual(expectedTypes, types) 
        
        # Check one type with two levels of options
        logging.debug("Testing the serialization of a message.")
        expectedOpts = [{'comment': 'Choose one among the possible values', 'options': [{'comment': 'Choose one or more among the possible values , in a comma separated string', 'type': 'MULTIPLEVALUE', 'name': 'Trigger_Group', 'possible_values': 'Calo,ID,Egamma,Muon,B-Jet,Jet,Tau,MissingET,MinBiass,Bphys'}], 'type': 'SINGLEVALUE', 'name': 'Trigger_Area', 'possible_values': 'Online,Offline,Trigger Group'}]
        opts = elisa.getMessageType('Trigger')
        self.assertEqual(expectedOpts, opts)
        
        # Check an inexistent type
        logging.debug("Testing accessing an unknown message type.")
        with self.assertRaises(ElisaError):
            elisa.getMessageType('UnexistentType')


    
if __name__ == '__main__':
    unittest.main()
