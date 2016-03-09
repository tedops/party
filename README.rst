#####
PARTY
#####

Python client for the Artifactory API

Usage
=====

Key Points
==========

* Configuration is pre-loaded from ``party_config.py``, but can be overridden at runtime
* A new class must first be instantiated
* Any properties returned from using a "find" or "get" method are assigned to the class instance
* Properties are NOT appended. To add multiple properties to a class, get them all in one call.

Some example code:

.. code:: python

    import party

    artifact = party.Party()

    artifact.artifactory_url = "http://myserver.com/api"  # <= Runtime config change

Additionally, passing a ``config`` parameter to ``Party()`` will work

.. code:: python

    PARTY_CONFIG = {
        'artifactory_url': 'https://myserver.com/api',
        'username': 'api',
        'password': 'password',
    }

    artifact = party.Party(config=PARTY_CONFIG)


Find Artifact by Name
=====================

.. code:: python

    myFile = "my-file.rpm"
    result = artifact.find(myFile)

Find Artifact By Properties
===========================

.. code:: python

    file_props = {
        "build.number": 999,
        "rpm.version": "1.0.0.999"
    }
    result = artifact.find_by_properties(file_props)

Find Artifact by Pattern
========================

.. code:: python

    result = artifact.find_by_pattern("erlang*R15B*.rpm")

Get Specific Artifact Properties
================================

.. code:: python

    specific_properties = [ "build.number", "rpm.version" ]
    result = artifact.get_properties(artifact, specific_properties)

Set Properties on an Artifact
=============================

.. code:: python

    new_properties = {
        "myKey": "myValue"
    }
    result = artifact.set_properties(artifact, new_properties)

CONFIGURING PARTY
=================

Party class instances load in the values from ``party_config.py``. However, those values can be overridden directly in the file, or at runtime using:

.. code:: python

    artifact = party.Party()
    artifact.CONFIG_KEY = "new value"

The following is a list of config keys (CONFIG_KEY above) and descriptions of their purposes:

::

    artifactory_url - Base URL to your Artifactory instance.
        search_prop - Artifactory API endpoint used for the property search.
        search_name - Artifactory API endpoint to access quick search.
       search_repos - Artifactory API endpoint to search for repositories.
           username - Username credential to use to connect to the Artifactory instance.
           password - Base64 encoded password credential used to connect to the Artifactory instance.
            headers - JSON (Python dict) of headers to send in the Artifactory queries.

