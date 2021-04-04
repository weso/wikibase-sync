from .common import MEDIAWIKI_API_URL
from rdflib import URIRef, Graph
from rdfsync.wb2rdf.conversion import Converter

graph = Graph()
graph.parse("tests/data/synchronization/atne.ttl", format='ttl')
converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph)
wikibase_id = 'Q4'  # human resource

triple_1_new_add = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                     URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                     URIRef('http://www.w3.org/2002/07/owl#InverseFunctionalProperty')))

triple_2_existent = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                      URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                      URIRef('http://www.w3.org/2002/07/owl#Class')))

triple_3_existent = ((URIRef('http://www.purl.org/hercules/asio/core#authors'),
                      URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                      URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))

triple_4_non_existent = ((URIRef('http://www.purl.org/hercules/asio/core#AdministrativePersonnel'),
                          URIRef('http://www.w3.org/2000/01/rdf-schema#domain'),
                          URIRef('http://www.purl.org/hercules/asio/core#ResearchPersonnel')))

triple_5_new_add = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                     URIRef('http://www.w3.org/2000/01/rdf-schema#domain'),
                     URIRef('http://www.w3.org/2004/02/skos/core#Concept')))


def test_add_new_triples():
    assert len(graph) == 2
    assert not graph.__contains__(triple_1_new_add)
    assert not graph.__contains__(triple_5_new_add)
    assert graph.__contains__(triple_2_existent)
    assert graph.__contains__(triple_3_existent)
    assert not graph.__contains__(triple_4_non_existent)

    converter.execute_synchronization(wb_id=wikibase_id)

    assert graph.__contains__(triple_1_new_add)
    assert graph.__contains__(triple_5_new_add)
    assert graph.__contains__(triple_2_existent)
    assert graph.__contains__(triple_3_existent)
    assert not graph.__contains__(triple_4_non_existent)
    assert len(graph) == 6  # with label and description
