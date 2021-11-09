Elisa client API
================


:mod:`Elisa` 
------------
.. autoclass:: src.elisa.Elisa
    :members:
    :show-inheritance:

:mod:`MessageRead`
-------------------------

.. autoclass:: src.messageRead.MessageRead
    :members: id, logbook, userName, author, date, subject, type, options, systemsAffected, body, host, hasReplies, replyTo, hasAttachments, attachments, status, threadHead, valid, encoding
    :show-inheritance:

:mod:`MessageInsert`
---------------------------

.. autoclass:: src.messageInsert.MessageInsert
    :members: author, subject, type, options, systemsAffected, body, attachments, status
    :show-inheritance:

:mod:`MessageReply`
--------------------------

.. autoclass:: src.messageReply.MessageReply
    :members: author, subject, options, systemsAffected, body, attachments, status
    :show-inheritance:

:mod:`MessageUpdate`
---------------------------

.. autoclass:: src.messageUpdate.MessageUpdate
    :members: body, attachments
    :show-inheritance:

:mod:`OptionsBuilder`
----------------------------

.. autoclass:: src.optionsBuilder.OptionsBuilder
    :members:
    :show-inheritance:

:mod:`SearchCriteria`
----------------------------

.. autoclass:: src.searchCriteria.SearchCriteria
    :members:
    :show-inheritance:

:mod:`exception`
-----------------------

.. automodule:: src.exception
    :members:
    :show-inheritance:

