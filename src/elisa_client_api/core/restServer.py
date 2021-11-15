#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : ELisA REST server
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : restServer.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 22/Nov/2012
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : RestServer
# Description   : Implements the Logbook interface to access the ELisA logbook backend 
#                 database through the REST server.
#--------------------------------------------------------------------------------------
# Copyright (c) 2012 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 22/Nov/2012: created.
# 08/Jan/2012: add authentication.
# 11/Feb/2013: add option to show attributes when searching for messages.
#--------------------------------------------------------------------------------------

import urllib.request
import urllib.parse
import urllib.error
import string
import logging

from .request import Request
from .serializer import Serializer
from elisa_client_api.exception import RestServerError


class RestServer(object):
    """ Accesses the ELisA logbook backend database through the REST server.
    """

    # ------------------
    # - Public methods -
    # ------------------
    def __init__(self, url, authentication):
        self.__url = url
        self.__authentication = authentication

            
    def getMessage(self, msgId):
        """ Queries the REST server to retrieve the logbook message with 
        the given ID.
        
        msgId: the message ID.
        Returns: an object of type MessageRead encapsulating the message
                 with the given ID.
        Throws: RestServerError if accessing the logbook fails.
        """
        url = self.__url + "messages/" + str(msgId) + "/"
        msgXml = Request(url, self.__authentication).get()
        return Serializer().deserialize(msgXml)
    
    
    def getAttachment(self, msgId, attachId):
        """ Queries the REST server to retrieve an attachment associated to 
        a messages. 

        msgId: message ID of the attachment to retrieve.
        attachId: the attachment ID.
        Returns: the attachment.
        Throws: RestServerError if accessing the logbook fails.
                ElisaError if the message has not attachments.
        """
        url = self.__url + "messages/" + str(msgId) + "/attachments/" + str(attachId)
        req = Request(url, self.__authentication)
        return req.get()
    
    
    def getAttachments(self, message):
        """ Queries the REST server to retrieve an attachment associated to 
        a messages. 

        message: object of type MessageRead with the attachments to retrieve.
        Returns: a list of tuples with the id, name and content of the attachments.
        Throws: RestServerError if accessing the logbook fails.
        """
        attchsList = []
        for attachment in message.attachments:
            attchsList.append((attachment[0], 
                               attachment[1], 
                               self.getAttachment(message.id, attachment[0])))
        
        return attchsList
    
    
    def searchMessages(self, criteria, showAttributes):
        """ Queries the REST server to retrieve the messages based 
        on a search criteria.
            
        criteria: object of type Criteria specifying the search 
                  filter.
        showAttributes: if true, it also returns the option and attachment
                        message fields.
        Returns: a list of objects of type MessageRead encapsulating 
                 the messages that meet the search criteria.
        Throws: RestServerError if accessing the logbook fails.
        """
    
        url = self.__url + "messages?" + urllib.parse.urlencode(criteria.getDict())
        msgXml = Request(url, self.__authentication).get()
        return Serializer().deserialize(msgXml)
            
    
    def insertMessage(self, message):
        """ Queries the REST server to insert a message into the logbook. 
            
        message: object of type MessageInsert to be inserted into the 
                 database.
        Returns: an object of type MessageRead encapsulating the message
                 inserted into the database.
        Throws: RestServerError if inserting the text message fails (but not 
                the attachments).
        """
        serializer = Serializer()
        msgInsertXml = serializer.serialize(message, "input_message")
        url = self.__url + "messages/"
        
        # If attachments are present, send a multipart request.
        # Otherwise, send a POST request.
        if not message.attachments or len(message.attachments) == 0:
            msgReadXml = Request(url, self.__authentication).post(msgInsertXml)
        else:
            msgReadXml = Request(url, self.__authentication).multipart((msgInsertXml, 'message'), message.attachments)
        
        return serializer.deserialize(msgReadXml)
        

    def updateMessage(self, message):
        """ Queries the REST server to updates a logbook message.
            
        message: object of type MessageUpdate to be updated into the
                 database.
        Returns: an object of type MessageRead encapsulating the message
                 updated into the database.
        Throws: RestServerError if updating the message fails.
                FileError if any of the attachment cannot be opened.
        """
            
        # If attachments and message is to be updated, send a multipart request.
        # If only the message is to be updated, send a PUT request.
        # If only an attachment is to be inserted, send a multipart to create attachment.
        if not message.body and not message.attachments and not message.date:
            return ""
        
        msgReadXml = None
        serializer = Serializer()
        if message.body:
            msgInsertXml = serializer.serialize(message, "message_body")
            url = self.__url + 'messages/' + str(message.id) + '/body'

            if message.attachments and len(message.attachments) > 0:
                msgReadXml = Request(url, self.__authentication).multipart((msgInsertXml, 'body'), message.attachments)
            else:
                msgReadXml = Request(url, self.__authentication).put(msgInsertXml)
        elif message.date:
            msgInsertXml = serializer.serialize(message, "date")
            url = self.__url + 'messages/' + str(message.id) + '/date'
            msgReadXml = Request(url, self.__authentication).put(message.date.encode('utf-8'))
        else:
            url = self.__url + 'messages/' + str(message.id) + '/attachments'
            msgReadXml = Request(url, self.__authentication).multipart(attachments=message.attachments)
        
        return serializer.deserialize(msgReadXml)
    
    
    def replyToMessage(self, message):
        """ Queries the REST server to insert a reply.
            
        message: object of type MessageReply to be inserted into the
                 database.
        Returns: an object of type MessageRead encapsulating the message
                 inserted into the database.
        Throws: RestServerError if accessing the logbook fails.
        """
        from messageInsert import MessageInsert
        
        # The reply message must inherit from the original message the type, subject, 
        # and if need be, the options and systems affected.
        rootMsg = self.getMessage(message.id)
       
        msgInsert = MessageInsert()
        msgInsert.author = message.author
        msgInsert.type = rootMsg.type
        msgInsert.systemsAffected = message.systemsAffected if message.systemsAffected else rootMsg.systemsAffected
        msgInsert.options = message.options if message.options else rootMsg.options
        msgInsert.subject = ('RE: ' + rootMsg.subject)
        msgInsert.body = message.body
        msgInsert.status = message.status
        msgInsert.attachments = message.attachments

        # A reply involves inserting a new message and it follows the same
        # logic and syntax.
        serializer = Serializer()
        msgReplyXml = serializer.serialize(msgInsert, "input_message")
        url = self.__url + "messages/" + str(message.id)

        # If attachments are present, send a multipart request.
        # Otherwise, send a POST request.
        if not msgInsert.attachments or len(msgInsert.attachments) == 0:
            msgReadXml = Request(url, self.__authentication).post(msgReplyXml)
        else:
            msgReadXml = Request(url, self.__authentication).multipart((msgReplyXml, 'message'), msgInsert.attachments)

        return serializer.deserialize(msgReadXml)


    def getMessageTypes(self):
        """ Queries the REST server to retrieve the message types. 
            
        Returns: a list of message types.
        Throws: RestServerError if accessing the logbook fails.
        """
        url = self.__url + "mt"
        typesXml = Request(url, self.__authentication).get()
        return Serializer().deserializeMessageTypes(typesXml)


    def getTypeOptions(self, msgType):
        """ Queries the REST server to retrieve the options for 
        a given message type. 
            
        msgType: the message type.
        Returns: a list of message types.
        Throws: RestServerError if accessing the logbook fails.
        """

        url = self.__url + "mt/" + urllib.parse.quote(msgType)  + "/opt"
        retval = ""
        try:
            typesXml = Request(url, self.__authentication).get()
            retval = Serializer().deserializeMessageTypeOptions(typesXml)
        except RestServerError as ex:
            # The returned code 404 indicates a missing resource. In this case
            # it means the type does not have any associated options.
            # If this is the case, simply ignore the exception 
            if 'HTTP Error 404' not in ex.__str__():
                raise ex
        
        return retval
    
    
    def getSystemsAffected(self):
        """ Queries the REST server to retrieve the possible systems 
        affected. 
            
        Returns: a list of possible systems affected.
        Throws: RestServerError if accessing the logbook fails.
        
        """ 
        url = self.__url + "sa"
        saXml = Request(url, self.__authentication).get()
        return Serializer().deserializeSystemsAffected(saXml)
    
    
    def getPredefinedSystemsAffected(self, msgType):
        """ Queries the REST server to retrieve the predefined systems 
        affected for a given message type. 
            
        msgType: a message type.
        Returns: a list of predefined systems affected for a message type.
        Throws: RestServerError if accessing the logbook fails.
        """ 
        url = self.__url + 'mt/' + urllib.parse.quote(msgType) + '/sa'
        retval = ""
        try:
            saXml = Request(url, self.__authentication).get()
            retval = Serializer().deserializeSystemsAffected(saXml)
        except RestServerError as ex:
            # The returned code 404 indicates a missing resource. In this case
            # it means the type does not have any predefined systems affected.
            # If this is the case, simply ignore the exception 
            if 'HTTP Error 404' not in ex.__str__():
                raise ex
        
        return retval

           
