"""Request interface for Artifactory."""
import base64
import logging

import requests


class PartyRequest(object):
    """Request interface for Artifactory.

    Args:
        artifactory_url (str): Artifactory Instance API URL, e.g.
            http://instance.jfrog.io/instance/api.
        headers (dict): Custom request headers.
        password (str): Authentication password base64 encoded.
        username (str): Authentication username.

    """

    def __init__(self,
                 artifactory_url='',
                 headers=None,
                 password='',
                 username=''):
        self.log = logging.getLogger(__name__)

        self.artifactory_url = artifactory_url
        self.password = password
        self.username = username

        self.headers = headers

    def request(self, endpoint, method='get', **kwargs):
        """Send request to Artifactory API.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.
            method (str): HTTP method to use, e.g. delete, get, head, options,
                patch, post.

        Returns:
            requests.models.Response: Artifactory response.

        Raises:
            requests.exceptions.HTTPError: Artifactory did not respond with a
                good status.

        """
        url = '/'.join([self.artifactory_url, endpoint])

        request_method = getattr(requests, method.lower())

        auth = (self.username, base64.b64decode(self.password).decode())
        response = request_method(
            url, auth=auth, headers=self.headers, **kwargs)

        self.log.debug('Artifactory response: [%d] %s', response.status_code,
                       response.text)

        response.raise_for_status()

        return response

    def delete(self, endpoint, **kwargs):
        """DELETE request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='delete', **kwargs)

    def get(self, endpoint, **kwargs):
        """GET request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='get', **kwargs)

    def head(self, endpoint, **kwargs):
        """HEAD request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='head', **kwargs)

    def options(self, endpoint, **kwargs):
        """OPTIONS request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='options', **kwargs)

    def patch(self, endpoint, **kwargs):
        """PATCH request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='patch', **kwargs)

    def post(self, endpoint, **kwargs):
        """POST request to Artifactory API endpoint.

        Args:
            endpoint (str): API endpoint to use, usually everything after
                ``api/``.

        """
        return self.request(endpoint, method='post', **kwargs)
