#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : ELisA authentication.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : authentication.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 18/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : Authentication
# Description   : Class providing the functionality to perform user authentication
#                 either using LDAP or SSO.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 18/Dec/2012: created.
#--------------------------------------------------------------------------------------

from elisa_client_api.exception import ArgumentError


class Authentication(object):
    """ Interface to the ELisA logbook database.
    """
    def __init__(self, username=None, password=None, ssocookie=None):
        """ Constructor

        username: user name.
        password: password
        type: authentication type; either 'ldap' or 'sso'.
        ssocookie: file with the sso-cookie created by auth-get-sso-cookie
        """
        self.__username = username
        self.__password = password
        self.__ssocookie = None

        if ssocookie != None:
            try:
                f = open(ssocookie)
                self.__ssocookie = f.read()
                f.close()
            except IOError as ex:
                raise ArgumentError("The cookie containing the sso authentication could not be read: " + str(ex))

            # Load the cookie
            import http.cookiejar
            cj = http.cookiejar.MozillaCookieJar()
            cj.load(filename=ssocookie, ignore_discard=True, ignore_expires=True)
            for cookie in cj:
                if cookie.name.startswith('_shibsession'):
                    self.__ssocookie = cookie.name + '=' + cookie.value

    # ------------------
    # - Public methods -
    # ------------------
    def addAuthentication(self, req):
        """ Adds the appropriate authentication header in the http request.
        """
        if self.__ssocookie != None:
            req.add_header('Cookie', self.__ssocookie)
        else:
            req.add_header("Authorization", "Basic %s" % self._getEncodedCredentials().decode())

    def addAuthenticationPy3(self, req):
        """ Adds the appropriate authentication header in the http request.
        """
        if self.__ssocookie != None:
            req.headers['Cookie'] = self.__ssocookie
        else:
            req.headers['Authorization'] = "Basic %s" % self._getEncodedCredentials().decode()

    def addAuthenticationToDict(self, d):
        """ Adds the appropriate authentication header in the http request.
        """

        if self.__ssocookie != None:
            d['Cookie'] = self.__ssocookie
        else:
            d['Authorization'] = "Basic %s" % self._getEncodedCredentials().decode()


    # -------------------
    # - Private methods -
    # -------------------
    def _getEncodedCredentials(self):
        """ Encodes the string username:password with basic 64
        """
        import base64
        return base64.encodestring(('%s:%s' % (self.__username, self.__password)).encode())[:-1]
