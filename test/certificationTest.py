#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Test for the ELisA certification.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : certificationTest.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 18/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : CertificationTest
# Description   : Test for the Elisa certification. 
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 18/Dec/2012: created.
#--------------------------------------------------------------------------------------

from builtins import str
import unittest
import logging 


class CertificationTest(unittest.TestCase):
    """ Test for the Elisa interface. 
    """
    def setUp(self):
        connection = "http://pcatd137.cern.ch:8080/elisa.api/api/"
        self._elisa = Elisa(connection)
        self._certification = Certification()
    
    # -------------------------
    # - Public methods: tests -
    # -------------------------
    def test_ldapAuthentication(self):
        """ Tests the operation 'get message by ID'.
        """
        self.assertEqual(id, msg.id)
        

    def test_ssoAuthentication(self):
        """ Tests that the operation 'get message by ID' fails when the
        ID value is invalid.
        """     
        id = -1
        logging.debug("Testing the operation: getMessage(" + str(id) + ")")
        with self.assertRaises(ElisaError):
            self._elisa.getMessage(id)
  
        
    # ---------------------------
    # - Private data attributes -
    # ---------------------------
    _elisa = None  # ELisA server.

    
if __name__ == '__main__':
    unittest.main()
