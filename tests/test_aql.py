"""Test AQL construction."""
from party.aql import Aql


def test_basic():
    """No arguments."""
    aql = Aql()
    assert aql.aql == 'items.find({})'


def test_more_arguments():
    """Pass some arguments in."""
    aql = Aql(
        criteria={'name': 'test'},
        domain_query='builds',
        fields=['name'],
        num_records=1,
        offset_records=1,
        order_and_fields={'$asc': ['repo']})
    assert aql.aql == ('builds'
                       '.find({"name": "test"})'
                       '.include("name")'
                       '.sort({"$asc": ["repo"]})'
                       '.limit(1)'
                       '.offset(1)')


def test_include():
    """Format ``.include()`` properly."""
    aql = Aql()
    assert aql.format_include() == ''

    aql.fields = ["name"]
    assert aql.format_include() == '.include("name")'

    aql.fields = ['name', 'repo']
    assert aql.format_include() == '.include("name", "repo")'


def test_limit():
    """Format ``.limit()`` properly."""
    aql = Aql()
    assert aql.format_limit() == ''

    aql.num_records = 0
    assert aql.format_limit() == ''

    aql.num_records = 10
    assert aql.format_limit() == '.limit(10)'


def test_offset():
    """Format ``.offset()`` properly."""
    aql = Aql()
    assert aql.format_offset() == ''

    aql.offset_records = 1
    assert aql.format_offset() == '.offset(1)'


def test_sort():
    """Format ``.sort()`` properly."""
    aql = Aql()
    assert aql.format_sort() == ''

    aql.order_and_fields = {'$asc': ['repo', 'name']}
    assert aql.format_sort() == '.sort({"$asc": ["repo", "name"]})'
