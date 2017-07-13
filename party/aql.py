"""Artifactory Query Language construction."""
import json
import logging


class Aql:
    """Artifactory Query Language.

    See `AQL User Guide`_ for full specification.

    .. _AQL User Guide: https://www.jfrog.com/confluence/display/RTF/Artifactory+Query+Language

    Attributes:
        criteria (dict): Used in ``.find()`` to search for artifacts, will be
            converted to JSON.
        domain_query (str, optional): Primary domain to perform query in, must
            be builds, entries, or items (default).
        fields (list, optional): Used in ``.include()`` to specify different
            fields included in results.
        num_records (int, optional): Used in ``.limit()`` to set the maximum
            number of results.
        offset_records (int, optional): Used in ``.offset()`` for first record
            to appear in results.
        order_and_fields (dict, optional): Used in ``.sort()`` for ordering
            results.

    """

    def __init__(  # pylint: disable=R0913,W0102
            self,
            criteria={},
            domain_query='items',
            fields=[],
            num_records=0,
            offset_records=0,
            order_and_fields={}):
        self.log = logging.getLogger(__name__)

        self.domain_query = domain_query
        self.criteria = criteria

        self.fields = fields
        self.num_records = num_records
        self.offset_records = offset_records
        self.order_and_fields = order_and_fields

    @property
    def aql(self):
        """Return string form of AQL statement.

        See `syntax`_ documentation for limitations. Limitation checking is not
        implemented here.

        .. _syntax: https://www.jfrog.com/confluence/display/RTF/Artifactory+Query+Language#ArtifactoryQueryLanguage-Syntax

        Examples:
            Basic form:

            >>> 'items.find({"repo": "myrepo"})'

        Returns:
            str: AQL statement, e.g. ``items.find({"repo": "myrepo"})``.

        """
        criteria = json.dumps(self.criteria)
        aql_statement = '{domain_query}.find({criteria})'.format(
            domain_query=self.domain_query, criteria=criteria)

        aql_statement += self.format_include()
        aql_statement += self.format_sort()
        aql_statement += self.format_limit()
        aql_statement += self.format_offset()

        self.log.debug('Full AQL statement: %s', aql_statement)
        return aql_statement

    def format_include(self):
        """Format ``.include()`` from :attr:`fields` for AQL.

        Examples:
            Basic form:

            >>> '.include("name")'

            Multiple fields form:

            >>> '.include("name", "repo")'

        Returns:
            str: ``.include()`` statement for AQL.

        """
        statement = ''

        if self.fields:
            fields = json.dumps(self.fields)
            fields = fields.lstrip('[').rstrip(']')

            statement = '.include({0})'.format(fields)

        self.log.debug('Include statement: %s', statement)
        return statement

    def format_limit(self):
        """Format ``.limit()`` from :attr:`num_records` for AQL.

        To paginate, use with :meth:`format_offset`.

        Examples:
            Basic form:

            >>> '.limit(100)'

        Returns:
            str: ``.limit()`` statement for AQL.

        """
        statement = ''

        if self.num_records:
            statement = '.limit({0:d})'.format(self.num_records)

        self.log.debug('Limit statement: %s', statement)
        return statement

    def format_offset(self):
        """Format ``.offset()`` from :attr:`offset_records` for AQL.

        Can be used for pagination when used with :meth:`format_limit`.

        Examples:
            Basic form:

            >>> '.offset(100)'

        Returns:
            str: ``.offset()`` statement for AQL.

        """
        statement = ''

        if self.offset_records:
            statement = '.offset({0:d})'.format(self.offset_records)

        self.log.debug('Offset statement: %s', statement)
        return statement

    def format_sort(self):
        """Format ``.sort()`` from :attr:`order_and_fields` for AQL.

        Examples:
            Basic form:

            >>> '.sort({"$asc" : ["repo","name"]})'

        Returns:
            str: ``.sort()`` statement for AQL.

        """
        statement = ''

        if self.order_and_fields:
            order_and_fields = json.dumps(self.order_and_fields)
            statement = '.sort({0})'.format(order_and_fields)

        self.log.debug('Sort statement: %s', statement)
        return statement
