#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Test for the ELisA interface.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisaTest.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 3/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : ElisaTest
# Description   : Test for the Elisa interface. 
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 03/Dec/2012: created.
#--------------------------------------------------------------------------------------

from __future__ import print_function
from builtins import str
import unittest
import logging 

from elisa import Elisa
from exception import ElisaError
from searchCriteria import SearchCriteria
from messageInsert import MessageInsert
from messageUpdate import MessageUpdate


class ElisaTest(unittest.TestCase):
    """ Test for the Elisa interface. 
    """
    def setUp(self):
        elisaCon = "https://pc-atd-elisa.cern.ch/elisa.api/api/"
        ssoCookiePath = '/afs/cern.ch/user/r/rmurillo/private/ssocookie.txt'
        self._elisa = Elisa(connection=elisaCon, ssocookie=ssoCookiePath)
    
    # -------------------------
    # - Public methods: tests -
    # -------------------------
    def test_getMessage(self):
        """ Tests the operation 'get message by ID'.
        """
        msgId = '132635'
        logging.debug("Testing the operation: getMessage(" + msgId + ")")
        msg = self._elisa.getMessage(msgId)
        self.assertEqual(msgId, msg.id)
        

    def test_getMessageWrongId(self):
        """ Tests that the operation 'get message by ID' fails for an invalid ID.
        """     
        msgId = -1
        logging.debug("Testing the operation: getMessage(" + str(msgId) + ")")
        self.assertRaises(ElisaError, self._elisa.getMessage, msgId)

 
    def test_searchMessages(self):
        """ Tests the operation 'search messages'.
        """
        logging.debug("Testing the operation: searchMessages()")
        criteria = SearchCriteria()
        criteria.author = "Alina Corso Radu"
        criteria.limit = 10
        criteria.subject = "Summary"
        criteria.systemsAffected = "DAQ"
        msgs = self._elisa.searchMessages(criteria)
        for msg in msgs: 
            self.assertEqual("Alina Corso Radu", msg.author)
            
        
    def test_getMessageAttachment(self):
        """ Tests the operation 'get message attachment'
        """
        from messageRead import MessageRead
        
        logging.debug("Testing the operation: get attachment")
        attachment = self._elisa.getAttachment(132635, 1239087)
        
        logging.debug("Testing the operation: get wrong attachment")
        self.assertRaises(ElisaError, self._elisa.getAttachment, 132635, -1)
        

    def test_insertMessage(self):
        """ Tests the operation 'insert message'.
        """
        import optionsBuilder as OB
        
        logging.debug("Testing the operation: insertMessage()")
        msgWrite = MessageInsert()
        msgWrite.body = "Unit test to verify the insertion of a message."
        msgWrite.type = "Trigger"
        msgWrite.subject = "Python API test"
        msgWrite.systemsAffected = ["DAQ"]

        ob = OB.OptionsBuilder()
        taOpt = ob.addOption('Trigger_Area', 'Trigger Group')
        taOpt.addOption('Trigger_Group', 'ID')
        taOpt.addOption('Trigger_Group', 'Calo')
        msgWrite.options = ob.toList()

        msgRead = self._elisa.insertMessage(msgWrite)
        self.assertEqual(msgWrite.body, msgRead.body)
        self.assertEqual(msgWrite.type, msgRead.type)
        self.assertEqual(msgWrite.subject, msgRead.subject)
        self.assertEqual(msgWrite.systemsAffected, msgRead.systemsAffected)
    
        logging.debug("Testing the operation: insert attachment")
        msgWrite.body = "Unit test to verify the insertion of a message with an attachment."        
        msgWrite.attachments = ["/afs/cern.ch/user/r/rmurillo/public/barcelona.jpg"]
        msgRead = self._elisa.insertMessage(msgWrite)
        #@TODO self.assertEqual()
  
  
    def test_updateMessages(self):
        """ Tests the operation 'update messages'.
        """
        print('Updating.......')
        id = 132635
        logging.debug("Testing the operation: updateMessage(" + str(id) + "). Only the body is updated.")
        msgUpdate = MessageUpdate(id)
        msgUpdate.body = "Unit test to verify the update of a message."
        self._elisa.updateMessage(msgUpdate)
    
        logging.debug("Testing the operation: updateMessage(" + str(id) + "). Only an attachment is inserted.")
        msgUpdate = MessageUpdate(id)
        msgUpdate.attachments = ["/Users/rmurillo/test.txt"]
        self._elisa.updateMessage(msgUpdate)    

        logging.debug("Testing the operation: updateMessage(" + str(id) + "). Body is updated and attachment inserted.")
        msgUpdate = MessageUpdate(id)
        msgUpdate.body = "Unit test to verify the update of a message and inserting an attachment."
        msgUpdate.attachments = ["/afs/cern.ch/user/r/rmurillo/public/test.txt"]
        self._elisa.updateMessage(msgUpdate)
        

    # ---------------------------
    # - Private data attributes -
    # ---------------------------
    _elisa = None  # ELisA server.

    
if __name__ == '__main__':
    unittest.main()
