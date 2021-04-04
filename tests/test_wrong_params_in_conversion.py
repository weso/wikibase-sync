from .common import MEDIAWIKI_API_URL
from rdfsync.wb2rdf.conversion import Converter
import pytest

converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl')
wikibase_id = 'Q5'


def test_wrong_params_in_constructor():
    with pytest.raises(ValueError):
        Converter(endpoint=MEDIAWIKI_API_URL, day_num=0)

    with pytest.raises(ValueError):
        Converter(endpoint=MEDIAWIKI_API_URL, input_format='non_existent')


def test_wrong_format_of_wb_item_prop():
    graph = converter.execute_synchronization(wb_id=wikibase_id)
    assert not graph  # non existent because there's no related link

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="A66")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="NON EXISTENT")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="QQNN")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="QQ")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="PP")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="PQ")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="QP")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="Q10P")

    with pytest.raises(ValueError):
        converter.execute_synchronization(wb_id="P10Q")
