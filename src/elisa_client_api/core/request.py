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

import requests
import os
import mimetypes

from elisa_client_api.exception import RestServerError


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
        headers = {
            'Accept': 'application/xml'
        }
        self.__authentication.addAuthenticationToDict(headers)

        try:
            response = requests.get(
                self.__url,
                headers = headers,
                verify = False,
            )
            self._checkSsoAuthen(response)
            return response.content
        except requests.exceptions.HTTPError as ex:
            # The returned code 302 is expected. The reason why is
            # explained in http://en.wikipedia.org/wiki/HTTP_302
            # if ex.code == 302:
            #     return ex.read()
            # Otherwise it is a valid error, raise it.
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except requests.URLRequired as ex: #?
            raise RestServerError(str(ex))


    def post(self, message):
        """ Makes a post request to insert a message.

        message: message to insert/post.
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
        """

        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/xml',
        }

        self.__authentication.addAuthenticationToDict(headers)

        try:
            response = requests.post(
                self.__url,
                data = message,
                headers = headers,
                verify = False,
            )
            self._checkSsoAuthen(response)
            return response.content
        except requests.exceptions.HTTPError as ex:
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except requests.exceptions.URLRequired as ex:
            raise RestServerError(str(ex))


    def put(self, message):
        """ Makes a put request to update a message.

        message: message to update/post.
        Returns: the data returned by the server.
        Throws: RestServerError if the request fails.
        """

        headers = {
            'Content-Type': 'application/xml',
            'Accept': 'application/xml',
        }

        self.__authentication.addAuthenticationToDict(headers)

        try:
            response = requests.put(
                self.__url,
                data = message,
                headers = headers,
                verify = False,
            )
            self._checkSsoAuthen(response)
            return response.content
        except requests.exceptions.HTTPError as ex:
            raise RestServerError(str(ex) + ". REST server error: " + ex.read().decode())
        except requests.exceptions.URLRequired as ex:
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
        #except urllib3.error.URLError as ex:
        #    raise RestServerError(str(ex))

    # -------------------
    # - Private methods -
    # -------------------
    def _checkSsoAuthen(self, response):
        # Is there a better way to detect this?
        content = response.content.decode()
        if '<!DOCTYPE html PUBLIC' in content and 'Sign in with your CERN account' in content:
            raise RestServerError("SSO authentication failed")

