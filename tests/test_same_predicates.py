from .common import MEDIAWIKI_API_URL
from rdflib import URIRef, Graph, Literal
from rdfsync.wb2rdf.conversion import Converter

graph = Graph()
graph.parse("tests/data/synchronization/sp.ttl", format='ttl')
converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph)
wikibase_id = 'Q11'  # country

subject_same_label = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                       URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                       Literal('country', lang='en')))

subject_same_description = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                             URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                             Literal(
                                 'This property indicates the nationality of a resource. '
                                 'The domain is not set so unpredicted resources within the ontology '
                                 'could be attached to countries.', lang='en')))

subject_same_triple = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                        URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                        URIRef('http://www.w3.org/2002/07/owl#Class')))

triple_non_existent = ((URIRef('http://www.purl.org/hercules/asio/core#AdministrativePersonnel'),
                        URIRef('http://www.w3.org/2000/01/rdf-schema#domain'),
                        URIRef('http://www.purl.org/hercules/asio/core#ResearchPersonnel')))


def test_same_predicates_update():
    assert len(graph) == 3
    assert not graph.__contains__(triple_non_existent)
    assert graph.__contains__(subject_same_label)
    assert graph.__contains__(subject_same_description)
    assert graph.__contains__(subject_same_triple)

    converter.execute_synchronization(wb_id=wikibase_id)

    assert len(graph) == 3
    assert not graph.__contains__(triple_non_existent)
    assert graph.__contains__(subject_same_label)
    assert graph.__contains__(subject_same_description)
    assert graph.__contains__(subject_same_triple)
    graph.serialize()
