import logging
import json
import requests
import urllib
import base64
import os

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .exceptions import UnknownQueryType
from .party_aql import find_by_aql
from .party_config import party_config
from .party_request import PartyRequest


class Party(PartyRequest):
    """Artifactory API interface.

    Attributes:
        artifactory_url (str): Artifactory Instance API URL, e.g.
            http://instance.jfrog.io/instance/api.
        headers (dict): Custom request headers.
        password (str): Authentication password base64 encoded.
        search_name (str): Artifact search endpoint (default: search/artifact).
        search_prop (str): Property search endpoint (default: search/prop).
        search_repos (str): Repositories list endpoint (default: repositories).
        username (str): Authentication username.

    """

    find_by_aql = find_by_aql

    def __init__(self, config={}, *args, **kwargs):
        super(Party, self).__init__(*args, **kwargs)

        self.log = logging.getLogger(__name__)

        self.files = []

        party_config.update(config)

        # Set instance variables for every value in party_config
        for k, v in party_config.items():
            existing_attribute = getattr(self, k, None)
            if not existing_attribute:
                setattr(self, '%s' % (k,), v)

    def query_artifactory(self, query, query_type='get', dry=False, **kwargs):
        """
        Send request to Artifactory API endpoint.
        @param: dry - Optional. Test run request.
        @param: query - Required. The URL (including endpoint) to send to the Artifactory API
        @param: query_type - Optional. CRUD method. Defaults to 'get'.
        @param: **kwargs - Extra keyword arguments to pass to :cls:`requests.models.Request`.
        """
        if dry:
            self.log.info('Would send "%s" request to: %s', query_type, query)
            content = json.dumps({
                'message': 'Dry mode enabled.',
                'query': query,
                'query_type': query_type
            })

            response = requests.models.Response()
            response.status_code = 200
            response._content = content.encode()

            return response

        auth = (self.username, base64.b64decode(self.password).decode())
        query_type = query_type.lower()

        if query_type == "get":
            response = requests.get(query, auth=auth, headers=self.headers, verify=self.certbundle)
        elif query_type == "put":
            response = requests.put(query, data=query.split('?', 1)[1], auth=auth, headers=self.headers, verify=self.certbundle)
        elif query_type == 'delete':
            response = requests.delete(query, auth=auth, headers=self.headers, verify=self.certbundle)
        elif query_type == "post":
            response = requests.post(query, auth=auth, headers=self.headers, verify=self.certbundle, **kwargs)
        else:
            raise UnknownQueryType('Unsupported query type: %s' % query_type)

        self.log.debug('Artifactory response: [%d] %s', response.status_code,
                       response.text)

        if not response.ok:
            return None

        return response

    def query_file_info(self, filename):
        """
        Send request to Artifactory API endpoint for file details.
        @param: filename - Required. The shortname of the artifact
        """
        query = "%s/storage/%s" % (self.artifactory_url, filename)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)

        return response

    def find_by_properties(self, properties):
        """
        Look up an artifact, or artifacts, in Artifactory by using artifact properties.
        @param: properties - List of properties to use as search criteria.
        """
        query = "%s/%s?%s" % (self.artifactory_url,
                              self.search_prop, urlencode(properties))
        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response

        response = json.loads(raw_response.text)

        for item in response['results']:
            for k, v in item.items():
                setattr(self, '%s' % (k,), v)

        if not response['results']:
            return None

        artifact_list = []
        for u in response['results']:
            artifact_list.append(os.path.basename(u['uri']))

        self.files = artifact_list
        setattr(self, 'count', len(artifact_list))

        return "OK"

    def find(self, filename):
        """
        Look up an artifact, or artifacts, in Artifactory by
        its filename.
        @param: filename - Filename of the artifact to search.
        """
        query = "%s/%s?name=%s" % (self.artifactory_url,
                                   self.search_name, filename)
        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)
        if len(response['results']) < 1:
            return None

        setattr(self, 'name', filename)
        setattr(self, 'url', json.dumps(response))

        return "OK"

    def get_properties(self, filename, properties=None):
        """
        Get an artifact's properties, as defined in the Properties tab in
        Artifactory.
        @param: filename - Filename of artifact of which to get properties.
        @param: properties - Optional. List of properties to help filter results.
        """
        if properties:
            query = "%s?properties=%s" % (filename, ",".join(properties))
        else:
            query = "%s?properties" % filename

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)
        for key, value in response.items():
            setattr(self, '%s' % (key,), value)

        return "OK"

    def get_file_info(self, filename):
        """
        Get an artifact's file info, as defined in the General tab in
        Artifactory.
        @param: filename - Filename of artifact of which to get file info.
        """

        response = self.query_file_info(filename)

        if response is None:
            return response

        setattr(self, 'file_info', response)
        return "OK"

    def get_file_stats(self, filename):
        """
        Get an artifact's file stats.
        @param: filename - Filename of artifact of which to get file info.
        """
        filename = '{0}?stats'.format(filename)

        response = self.query_file_info(filename)

        setattr(self, 'file_stats', response)
        return "OK"

    def get_storage_info(self):
        query = "%s/storageinfo" % (self.artifactory_url)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)

        setattr(self, 'storage_info', response)

        return 'OK'

    def set_properties(self, file_url, properties):
        """
        Set properties on an artifact.
        @param: file_url - URL of artifact on which to set properties.
        @param: properties - JSON list of properties to set on the artifact.
        """
        query = "%s?properties=%s" % (
            file_url, urlencode(properties).replace('&', '|'))
        response = self.query_artifactory(query, "put")
        if response is None:
            return response

        return "OK"

    def get_repositories(self, repo_type=None):
        """
        Helper method to get repository names. Defaults to all.
        @param: repo_type - type of repository to return (local, remote, virtual)
        """
        # Current Artifactory API doesn't allow multiple types to be
        # selected, so let's allow specifying at least one type.
        repositories = []
        if repo_type is None:
            query = "%s/%s" % (self.artifactory_url, self.search_repos)
        else:
            query = "%s/%s?type=%s" % (self.artifactory_url,
                                       self.search_repos, repo_type)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)

        for line in response:
            for item in line:
                repositories.append(line["key"])

        if repositories:
            return repositories

        return None

    def find_by_pattern(self, filename, specific_repo=None, repo_type=None, max_depth=10):
        """
        Look up an artifact, or artifacts, in Artifactory by
        its partial filename (can use globs).
        @param: filename - Required. Filename or partial filename to search.
        @param: specific_repo - Optional. Name of Artifactory repo to search.
        @param: repo_type - Optional. Values are local|virtual|remote.
        @param: max_depth - Optional. How many directories deep to search. Defaults to 10.
        """

        # Ensure filename is specified
        if not filename:
            errmsg = "No filename specified."
            raise ValueError(errmsg)
            return False

        # Validate specified repo type
        repo_types = ["local", "virtual", "remote", None]
        if repo_type not in repo_types:
            errmsg = "Invalid repo_type '%s' specified (valid types: 'local', 'virtual', 'remote', 'None'.)" % repo_type
            raise ValueError(errmsg)
            return False

        # Add in bookend globs to aid the search, but not if
        # they're already there, cuz Artifactory doesn't like that
        if filename[-1] != "*":
            filename = "%s*" % filename
        if filename[0] != "*":
            filename = "*%s" % filename

        # Create pattern list
        patterns = []
        # Adjust max_depth to determine how many (inclusive) directories deep
        # on the path to search
        for p in range(0, max_depth):
            patterns.append("*/" * p)

        if specific_repo is not None:
            repos = [specific_repo]
        else:
            repos = self.get_repositories(repo_type)

        # Cycle through each pattern in each repo to find the artifact
        results = []
        for repo in repos:
            for pattern in patterns:
                query = "%s/search/pattern?pattern=%s:%s%s" % (
                    self.artifactory_url, repo, pattern, filename)
                raw_response = self.query_artifactory(query)
                if raw_response is None:
                    return raw_response
                response = json.loads(raw_response.text)

                try:
                    if response['files']:
                        for i in response['files']:
                            results.append("%s/%s" % (response['repoUri'], i))
                except KeyError:
                    pass

        if not results:
            return None

        # Set the class 'files' variable to have the list of found artifacts
        self.files = results
        return "OK"
