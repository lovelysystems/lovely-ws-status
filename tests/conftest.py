import json
import pytest

from lovely.ws import status


@pytest.fixture(autouse=True)
def doctest_inject(doctest_namespace):
    """Inject some helper methods for the doctests."""

    # status handlers are global, so clear them before each test
    status.STATUS_HANDLERS.clear()

    doctest_namespace['print_json'] = print_json
    doctest_namespace['print_dict'] = print_dict


def print_json(o, sort_keys=True):
    if isinstance(o, bytes):
        o = o.decode("utf-8")
    o = json.loads(o)
    print_dict(o, sort_keys)


def print_dict(d, sort_keys=True):
    print(json.dumps(d, indent=4, sort_keys=sort_keys, separators=(',', ': ')))
