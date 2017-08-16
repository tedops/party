"""Interface for AQL searches."""
import logging

from .aql import Aql

LOG = logging.getLogger(__name__)


def find_by_aql(self, **kwargs):
    """Find artifacts using AQL.

    Args:
        **kwargs: See :class:`party.aql.Aql` for arguments.

    Returns:
        object: Results from AQL search.

    """
    aql = Aql(**kwargs)

    url = '/'.join([self.artifactory_url, 'search/aql'])

    old_content_type = self.headers['Content-type']
    self.headers['Content-type'] = 'text/plain'
    results = self.query_artifactory(url, data=aql.aql, query_type='post')
    self.headers['Content-type'] = old_content_type

    return results.json()
