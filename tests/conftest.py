import pytest
from mock import Mock

from posixpath import join as urljoin
from requests import HTTPError
from urllib.parse import urlencode, quote
from requests import Request

from pyairtable.api import Api, Table, Base
from collections import OrderedDict


@pytest.fixture
def json_matcher():
    """Returns func that when called returns a matcher for a mocker response to match provided json"""

    def _matcher(json_data):
        def __matcher(request):
            return sorted(request.json().items()) == sorted(json_data.items())

        return __matcher

    return _matcher


@pytest.fixture
def url_builder():
    """Builds Airtable Api Url Manually for mock testing"""

    def _url_builder(base_url, params=None, paths=[]):
        url = urljoin(base_url, *paths)
        if params:
            params = OrderedDict(sorted(params.items()))
            url = Request("notused", url, params=params).prepare().url
        return url

    return _url_builder


@pytest.fixture
def constants():
    return dict(
        API_KEY="FakeApiKey", BASE_ID="appJMY16gZDQrMWpA", TABLE_NAME="Table Name"
    )


@pytest.fixture()
def api(constants):
    return Api(constants["API_KEY"])


@pytest.fixture()
def base(constants):
    return Base(constants["API_KEY"], constants["BASE_ID"])


@pytest.fixture()
def table(constants):
    return Table(constants["API_KEY"], constants["BASE_ID"], constants["TABLE_NAME"])


@pytest.fixture
def mock_records():
    return [
        {
            "id": "recH73JJvr7vv1234",
            "fields": {"SameField": 1234, "Value": "abc"},
            "createdTime": "2017-06-06T18:30:57.000Z",
        },
        {
            "id": "recyXhbY4uax4567",
            "fields": {"SameField": 456, "Value": "def"},
            "createdTime": "2017-06-06T18:30:57.000Z",
        },
        {
            "id": "recyXhbY4uax891",
            "fields": {"SameField": 789, "Value": "xyz"},
            "createdTime": "2017-06-06T18:30:57.000Z",
        },
    ]


@pytest.fixture
def mock_response_single(mock_records):
    return mock_records[0]


@pytest.fixture
def mock_response_batch(mock_records):
    return {"records": mock_records * 2}


@pytest.fixture
def mock_response_list(mock_records):
    return [
        {"records": mock_records[0:2], "offset": "recuOeLpF6TQpArJi"},
        {"records": [mock_records[2]]},
    ]


@pytest.fixture
def mock_response_iterator(mock_response_list):
    """Each call will return the next response in mock_response_list"""
    i = iter(mock_response_list)

    def _response_iterator(request, context):
        return next(i)

    return _response_iterator


def http_error():
    raise HTTPError("Not Found")


@pytest.fixture
def response():
    response = Mock()
    response.raise_for_status.side_effect = http_error
    response.url = "page%20url"
    return response
