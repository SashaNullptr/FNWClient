The Telegram Streaming Analytics Module
---------------------------------------

.. currentmodule:: services.streaming

Design Notes
^^^^^^^^^^^^
The Telgram Interface makes use of the Telegram Client API to grab message data
and run analytics.

API Docs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoflask:: services.streaming.backend:app
   :undoc-static:

Implementation Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: services.streaming.lib.StreamingAnalytics
    :members:
