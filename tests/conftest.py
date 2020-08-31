from unittest import mock

import pytest
from wikidataintegrator import wdi_core

from wbsync.external.uri_factory_mock import URIFactory
from wbsync.triplestore import WikibaseAdapter


FACTORY = URIFactory()


class IDGenerator():
    def __init__(self):
        self.curr_id = 0

    def generate_id(self, _, **kwargs):
        try:
            etype = kwargs['entity_type']
            self.curr_id += 1
            str_id = str(self.curr_id)
            return 'Q' + str_id if etype == 'item' else 'P' + str_id
        except KeyError:
            pass

@pytest.fixture()
def id_generator():
    return IDGenerator()


@pytest.fixture(autouse=True)
def reset_state(id_generator):
    id_generator.curr_id = 0
    FACTORY.reset_factory()


@pytest.fixture
def mocked_adapter(id_generator):
    with mock.patch.object(WikibaseAdapter, '__init__', lambda slf, a, b, c, d: None):
        adapter = WikibaseAdapter('', '', '', '')
        adapter._init_callbacks()
        writer_mock = mock.MagicMock()
        writer_mock.write = mock.MagicMock(side_effect=id_generator.generate_id)
        writer_mock.update = mock.MagicMock()
        adapter._local_item_engine = mock.MagicMock(return_value=writer_mock)
        adapter._local_login = mock.MagicMock()
        adapter._mappings_prop = mock.MagicMock()
        yield adapter
