from .common import MEDIAWIKI_API_URL
from rdfsync.wb2rdf.conversion import Converter

converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', day_num=365)
items_changed_during_last_year_list \
    = ['Q19', 'Q13', 'Q21', 'Q15', 'P26', 'Q12', 'Q18', 'P30', 'P11', 'Q20', 'Q14', 'Q17', 'Q11', 'Q5', 'Q16']


def test_list_of_items_to_change():
    items_list = converter.get_items_properties_to_sync()
    print('hihi\n' + str(items_list))
    assert items_list.issubset(items_changed_during_last_year_list)
