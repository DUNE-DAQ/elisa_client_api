#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : HTTP request
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : request.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 19/Dec/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : Request
# Description   : Encapsulates the functionality to perform HTTP requests. 
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 19/Dec/2012: created.
# 08/Jan/2012: add authentication
#--------------------------------------------------------------------------------------

import urllib.request, urllib.parse, urllib.error
import requests
import os
import mimetypes

from .exception import RestServerError


class Request(object):
    """ Encapsulates the functionality to perform HTTP requests.
    """
    def __init__(self, url, authentication):
        """ Constructor
            
        url: URL to make the request to. 
        """
        self.__url = url
        self.__authentication = authentication
    
    # -----------------------------
    # - Public methods: Interface -
    # -----------------------------
    def get(self):
        """ Makes a get request with the params in the argument.
            
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
        """
        req = urllib.request.Request(self.__url)
        self.__authentication.addAuthentication(req)
        req.add_header('Accept', 'application/xml')
        req.get_method = lambda: 'GET'
        
        try:
            response = urllib.request.urlopen(req).read()
            self._checkSsoAuthen(response)
            return response
        except urllib.error.HTTPError as ex:
            # The returned code 302 is expected. The reason why is 
            # explained in http://en.wikipedia.org/wiki/HTTP_302 
            if ex.code == 302:
                return ex.read()
            # Otherwise it is a valid error, raise it.
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except urllib.error.URLError as ex:
            raise RestServerError(str(ex))
        
        
    def post(self, message):
        """ Makes a post request to insert a message.
            
        message: message to insert/post.
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
        """
        req = urllib.request.Request(self.__url,message)
        self.__authentication.addAuthentication(req)
        req.add_header('Content-Type', 'application/xml')
        req.add_header('Accept', 'application/xml')
        req.get_method = lambda: 'POST'

        try:
            response = urllib.request.urlopen(req).read()
            self._checkSsoAuthen(response)
            return response
        except urllib.error.HTTPError as ex:
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except urllib.error.URLError as ex:
            raise RestServerError(str(ex))
        
        
    def put(self, message):
        """ Makes a put request to update a message.
            
        message: message to update/post.
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
        """
        req = urllib.request.Request(self.__url,message)
        self.__authentication.addAuthentication(req)
        req.add_header('Content-Type', 'application/xml')
        req.add_header('Accept', 'application/xml')
        req.get_method = lambda: 'PUT'

        try:
            response = urllib.request.urlopen(req).read()
            self._checkSsoAuthen(response)
            return response
        except urllib.error.HTTPError as ex:
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except urllib.error.URLError as ex:
            raise RestServerError(str(ex))
        
        
    def multipart(self, message=None, attachments=None):
        """ Makes a multipart request to insert a message and/or attachments.
            
        message: a tuple containing the message to insert/post and the 
                 content disposition name.
        attachments: attachments to insert.
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
                FileError if any of the attachment cannot be opened.
        """
        session = requests.Session()
        files={}        
        if message != None:
            files[message[1]] = (None,message[0],'application/xml')
        count=0
        for attachment in attachments:
            files['file'+str(count)] = (os.path.basename(attachment), open(attachment, 'rb'), mimetypes.guess_type(attachment)[0] or 'application/octet-stream')
        request = requests.Request('POST', self.__url, files=files)
        prepped = session.prepare_request(request)
        self.__authentication.addAuthenticationPy3(prepped)        
        #print(prepped.body.decode('ascii'), prepped.headers)
        
        try:
            response = session.send(prepped, verify=False)
            #self._checkSsoAuthen(response.content)
            #print(response.text)
            return response.content
        except requests.exceptions.HTTPError as ex:
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        #except urllib.error.URLError as ex:
        #    raise RestServerError(str(ex))
        
    # -------------------    
    # - Private methods -
    # -------------------
    def _checkSsoAuthen(self, response):
        # Is there a better way to detect this?
        if '<!DOCTYPE html PUBLIC' in response.decode() and 'Sign in with your CERN account' in response.decode():
            raise RestServerError("SSO authentication failed");()

