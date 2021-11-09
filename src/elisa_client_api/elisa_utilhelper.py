#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Title         : Utilities helper.
# Project       : ATLAS, TDAQ, ELisA
#--------------------------------------------------------------------------------------
# File          : elisa_utilhelper.py
# Author        : Raul Murillo Garcia, raul.murillo.garcia@cern.ch
# Created       : 16/Jan/2013
# Revision      : 0 $
#--------------------------------------------------------------------------------------
# Class         : 
# Description   : Compendium of helper functions used by the Elisa utilities.
#                 Note: mandatory arguments should be handled differently.
#--------------------------------------------------------------------------------------
# Copyright (c) 2013 by University of California, Irvine. All rights reserved.
#--------------------------------------------------------------------------------------
# Modification history:
# 16/Jan/2013: created.
# 11/Feb/2013: add option to show attributes when searching for messages. 
#--------------------------------------------------------------------------------------


def parseCredentials(cmlArgs):
    args = dict()
    # SSO has higher priority
    if None != cmlArgs.sso:
        args['ssocookie'] = cmlArgs.sso
        return args
    
    username = None
    password = None
    # If no authentication credentials have been defined, get the user name
    # from the environment and ask for the password. If credentials have been
    # specified, check if the password is also defined.
    if None == cmlArgs.ldap:
        import getpass
        username = getpass.getuser()
        password = getpass.getpass("Password for " + username + ": ")        
    else:
        pos = cmlArgs.ldap.find(':')
        if pos != -1:
            username = cmlArgs.ldap[:pos]
            password = cmlArgs.ldap[pos+1:]
        else:
            import getpass
            username = cmlArgs.ldap
            password = getpass.getpass("Password for " + username + ": ")
        
    args['username'] = username
    args['password'] = password
    
    return args


def buildCommandLineArguments(utilName, cmlArgs, mandatory):
    from optparse import OptionParser
    
    usage = 'usage: ' + utilName + ' [options] args'
    parser = OptionParser(usage=usage,
                          epilog='In case of errors or bugs, please send an email to ' \
                          'atlas-tdaq-cc-wg@cern.ch')


    for arg in cmlArgs:
        addOption = {
            'version': lambda: parser.add_option('--version', 
                                                dest='version', 
                                                action="store_true", 
                                                default=False,
                                                help='print information about program name, version, etc'),
            'verbosity': lambda: parser.add_option('-v', '--verbose',
                                                type='int', 
                                                dest='verbosity', 
                                                metavar='LEVEL',
                                                default=1,
                                                help='sets the verbosity level [0-4]'),

            'server': lambda: parser.add_option('-s', '--server', 
                                                type='string', 
                                                dest='server', 
                                                metavar='SERVER',
                                                default=getElisaServer(None),
                                                help='URL of the EliSA REST server (i.e. ' \
                                                'https://pc-atd-elisa.cern.ch). If not specified, the main' \
                                                'EliSA server in P1 or GPN depending on user location.'),
            'sso': lambda: parser.add_option('-o', '--sso-credential', 
                                                type='string', 
                                                dest='sso', 
                                                metavar='SSO',
                                                help='path to a COOKIE file with the user credentials, as generated ' \
                                                'by the CERN SSO cookie tool (if not available already, you need to install auth-get-sso-cookie). ' \
                                                'MANDATORY when interacting with the GPN EliSA instance (https://atlasop.cern.ch).'),
            'ldap': lambda: parser.add_option('-c', '--ldap-credential', 
                                                type='string', 
                                                dest='ldap', 
                                                metavar='USERNAME:PASSWORD',
                                                help='user credential in the form USERNAME:PASSWORD or USERNAME. If only ' \
                                                'the username is provided, the password will be asked interactively.'),
            'logbook': lambda: parser.add_option('-k', '--logbook', 
                                                type='string', 
                                                dest='logbook', 
                                                metavar='LOGBOOK',
                                                help='logbook name. If argument is not provided  ' \
                                                'the default ATLAS value is used for the logbook.'),
            'id': lambda: parser.add_option('-i', '--id', 
                                                type='int', 
                                                dest='id', 
                                                metavar='ID',
                                                help='message unique ID'),
            'username': lambda: parser.add_option('-u', '--username', 
                                                type='string', 
                                                dest='username', 
                                                metavar='USER',
                                                help='message user name'),
	   'date': lambda: parser.add_option('-d', '--date', 
                                                type='string', 
                                                dest='date', 
                                                metavar='DATE',
                                                help='message date and time use format dd-mm-yyyy HH:mm:ss'),
            'author': lambda: parser.add_option('-a', '--author', 
                                                type='string', 
                                                dest='author', 
                                                metavar='AUTHOR',
                                                help='message author. If the author string is missing the author is ' \
                                                'evinced by user credential. N.B. space handling works both as: ' \
                                                '-a Jhon\ Do or -a "Jhon Do"'),
            'subject': lambda: parser.add_option('-j', '--subject', 
                                                type='string', 
                                                dest='subject', 
                                                metavar='SUBJECT',
                                                help='message subject'),
            'type': lambda: parser.add_option('-y', '--type', 
                                                type='string', 
                                                dest='type', 
                                                metavar='TYPE',
                                                help='message type.'),
            'systems': lambda: parser.add_option('-e', '--systems-affected', 
                                                type='string', 
                                                dest='systems', 
                                                metavar='SYSTEMS',
                                                help='message systems affected.'),
            'options': lambda: parser.add_option('-p', '--options', 
                                                type='string', 
                                                dest='options', 
                                                action="append",
                                                metavar='OPTIONS',
                                                help="option value in a key-value form (i.e. -o \"Trigger Area=Trigger Group\"). " \
                                                "Inner options can be expressed with a '.' notation between parent and inner " \
                                                "option name: -o \"Trigger Area.Trigger Group=VALUE\". This option can be used " \
                                                "multiple times."),
            'body': lambda: parser.add_option('-b', '--body', 
                                                type='string', 
                                                dest='body', 
                                                metavar='BODY',
                                                help='string with the message body.'),
            'bodyFile': lambda: parser.add_option('-z', '--body-file', 
                                                type='string', 
                                                dest='bodyFile', 
                                                metavar='BODY',
                                                help='path to a file with a text representation of the message body.'),
            'status': lambda: parser.add_option('-x', '--status', 
                                                type='string', 
                                                dest='status',
                                                metavar='STATUS',
                                                help='message status (closed or open). Default value: open.'),
            'statusReply': lambda: parser.add_option('-x', '--status', 
                                                type='string', 
                                                dest='statusReply',
                                                default='open',
                                                metavar='STATUS',
                                                help="message status. Possible values: 'open' or 'closed'. " \
                                                "If the status='closed', all the messages belonging to the THREAD " \
                                                "change status to CLOSED."),
            'since': lambda: parser.add_option('-f', '--date-from', 
                                                type='string', 
                                                dest='since', 
                                                metavar='FROM',
                                                help='initial date of the search. Format: DD/MM/YYYY HH:MM:ss.'),
            'to': lambda: parser.add_option('-t', '--date-to', 
                                                type='string', 
                                                dest='to', 
                                                metavar='TO',
                                                help='end date of the search. Format: DD/MM/YYYY HH:MM:ss.'),
            'interval': lambda: parser.add_option('-n', '--interval', 
                                                type='string', 
                                                dest='interval', 
                                                metavar='Nm',
                                                help="time interval. Current Server implementation only support month " \
                                                "interval. Format: NumberUnit: i.e. 3m = 3 months, 12m = 12 months, etc. " \
                                                "Could be evolved to support different time units (7 days = 7d, 3 weeks = 3w). " \
                                                "If not specified, the search is done on the last 3 months. "),
            'attributes': lambda: parser.add_option('-r', '--attributes', 
                                                dest='attributes', 
                                                action="store_true", 
                                                default=False,
                                                help='if specified when defining a search criteria, it returns the message attributes, ' \
                                                'that is, the option and attachment fields.'),
            'limit': lambda: parser.add_option('-l', '--limit',
                                                type='int', 
                                                dest='limit', 
                                                metavar='COUNT',
                                                default=10,
                                                help='maximum number of messages retrieved. By default 10.'),
            'attachmentsDst': lambda: parser.add_option('-m', '--attachment-path', 
                                                type='string', 
                                                dest='attachmentsDst', 
                                                metavar='PATH',
                                                help='path to download the attachments to. If this option is not ' \
                                                'specified, the attachments are not downloaded. If a value is not ' \
                                                'provided for this option, the attachments are stored in the current path'),
            'attachmentsSrc': lambda: parser.add_option('-m', '--attachment-file', 
                                                type='string', 
                                                action="append",
                                                dest='attachmentsSrc', 
                                                metavar='PATH',
                                                help='path to a file to be attached to the messages. ' \
                                                'This option can be used multiple times.')
            }[arg]()
            
    options, args = parser.parse_args()
            
    # Make sure all mandatory arguments have been defined.
    for manArg in mandatory:
        if not options.__dict__[manArg]:
            parser.error('missing mandatory argument: --' + manArg)
            exit(-1)
            
    return parser, options

            
def getLoggingLevel(level):
    """ Converts the command line verbosity level into a level for the logging module
    
    The two extreme logging levels are DEBUG (10) and logging.CRITICAL (50). 
    Map this to the verbosity level of command line argument: [0-4]
    """
    import logging
    return (logging.CRITICAL - logging.DEBUG) - level * 10 + 1


def getElisaServer(cmdlServer):
    import os

    if None != cmdlServer:
        return cmdlServer
    else:
        return 'https://np-vd-coldbox-elog.cern.ch'
 
def getElisaURL():
    import os
    if None == os.environ.get('DONT_USE_ELISA_MERGED'):
        return '/elisa/api/'
    else:
        return '/elisa.api/api/'

def parseOptions(options, parser):
    if not options:
        return options

    # Pre-arrange and sort options as a list with each options defined as:
    # [name, value] or for inner options
    # [name, innerName, value], [name, innerName, innerName, value], etc.
    
    listOpts = list()
    listInnerOpts = list()
    for option in options:
        # Separate key and value
        pair = option.strip().split('=')
        # Make sure the option name and value are properly defined, that is, name=value
        # 'option=' results in len=2 and pair[1]="". Check also for this condition.
        if len(pair) != 2 or not pair[1]:
            parser.error('invalid value format of argument --options')
            sys.exit()
        listOpts.append((pair[0].strip(), pair[1].strip()))

    # Sort the option name (including the inner name)
    listOpts.sort(key=lambda tup: tup[0])
#    import pprint
#    pp = pprint.PrettyPrinter(indent=2)
#    pp.pprint(listOpts)

    from optionsBuilder import OptionsBuilder
    obroot = OptionsBuilder()
    
    # Use a hash table with the option name as the key and the 
    # corresponding option builder as value. This schema assumes
    # the ordering above so that an inner option always has the
    # parent option builder available in the hash table.
    dirOBs = dict()
    for option in listOpts:
        name = option[0]
        value = option[1]
        if not '.' in name:
            dirOBs[name] = obroot.addOption(name, value)
        else:
            parts = name.rsplit(".", 1)
            dirOBs[name] = dirOBs[parts[0]].addOption(parts[1], value)
        
    return obroot.toList()

