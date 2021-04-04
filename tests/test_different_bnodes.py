from .common import MEDIAWIKI_API_URL
from rdflib import URIRef, Graph, Literal, BNode
from rdfsync.wb2rdf.conversion import Converter
from rdflib.namespace import XSD

graph = Graph()
graph.parse("tests/data/synchronization/db.ttl", format='ttl')
converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph)
wikibase_id = 'Q19'  # Example with one bnode
wikibase_id_without_bnode = 'Q11'  # country

triple_1_bnode = ((URIRef('http://www.w3.org/2002/07/owl#Example'),
                   URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                   URIRef('http://www.w3.org/2002/07/owl#Class')))

triple_2_bnode = ((URIRef('http://www.w3.org/2002/07/owl#Example'),
                   URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                   URIRef('http://www.w3.org/2002/07/owl#Thing')))

triple_3_bnode = ((BNode('ub1bL8C19'),
                   URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                   URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))

triple_4_bnode = ((BNode('ub1bL13C20'),
                   URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                   URIRef('http://www.w3.org/2002/07/owl#hasKey')))

triple_5_bnode = ((BNode('ub1bL8C19'),
                   URIRef('http://www.w3.org/2002/07/owl#onClass'),
                   URIRef('http://www.w3.org/2002/07/owl#Alumno')))

triple_6_bnode = ((BNode('ub1bL13C20'),
                   URIRef('http://www.w3.org/2002/07/owl#onDataRange'),
                   URIRef('http://www.w3.org/2002/07/owl#Professor')))

triple_7_bnode = ((BNode('ub1bL8C19'),
                   URIRef('http://www.w3.org/2002/07/owl#cardinality'),
                   Literal('2.0')))

triple_8_bnode = ((BNode('ub1bL13C20'),
                   URIRef('http://www.w3.org/2002/07/owl#qualifiedCardinality'),
                   Literal('2.0')))

new_predicate_label = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                        URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                        Literal('country', lang='en')))

new_predicate_description = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                              URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                              Literal(
                                  'This property indicates the nationality of a resource. '
                                  'The domain is not set so unpredicted resources within the ontology '
                                  'could be attached to countries.', lang='en')))

new_predicate_triple = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                         URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                         URIRef('http://www.w3.org/2002/07/owl#Class')))


def test_update_graph_with_new_bnodes():
    assert len(graph) == 10
    assert graph.__contains__(triple_1_bnode)
    assert graph.__contains__(triple_2_bnode)
    # works locally but not in travis because of random generated uid
    # assert graph.__contains__(triple_3_bnode)
    # assert graph.__contains__(triple_4_bnode)
    # assert graph.__contains__(triple_5_bnode)
    # assert graph.__contains__(triple_6_bnode)
    # assert graph.__contains__(triple_7_bnode)
    # assert graph.__contains__(triple_8_bnode)

    converter.execute_synchronization(wb_id=wikibase_id)
    # old bnodes deleted, new bnodes added
    assert len(graph) == 11
    assert graph.__contains__(triple_1_bnode)
    assert graph.__contains__(triple_2_bnode)
    assert not graph.__contains__(triple_3_bnode)
    assert not graph.__contains__(triple_4_bnode)
    assert not graph.__contains__(triple_5_bnode)
    assert not graph.__contains__(triple_6_bnode)
    assert not graph.__contains__(triple_7_bnode)
    assert not graph.__contains__(triple_8_bnode)


def test_update_graph_without_bnodes():
    graph2 = Graph()
    graph2.parse("tests/data/synchronization/db.ttl", format='ttl')
    converter2 = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph2)
    assert graph2.__contains__(triple_1_bnode)
    assert graph2.__contains__(triple_2_bnode)
    assert not graph2.__contains__(new_predicate_triple)
    assert not graph2.__contains__(new_predicate_description)
    assert not graph2.__contains__(new_predicate_label)
    # works locally but not in travis because of random generated uid
    # assert graph2.__contains__(triple_3_bnode)
    # assert graph2.__contains__(triple_4_bnode)
    # assert graph2.__contains__(triple_5_bnode)
    # assert graph2.__contains__(triple_6_bnode)
    # assert graph2.__contains__(triple_7_bnode)
    # assert graph2.__contains__(triple_8_bnode)

    converter2.execute_synchronization(wb_id=wikibase_id_without_bnode)
    # old bnodes deleted, new bnodes added
    assert len(graph2) == 13
    assert graph2.__contains__(triple_1_bnode)
    assert graph2.__contains__(triple_2_bnode)
    assert not graph2.__contains__(triple_3_bnode)
    assert not graph2.__contains__(triple_4_bnode)
    assert not graph2.__contains__(triple_5_bnode)
    assert not graph2.__contains__(triple_6_bnode)
    assert not graph2.__contains__(triple_7_bnode)
    assert not graph2.__contains__(triple_8_bnode)
    # new added triples
    assert graph2.__contains__(new_predicate_triple)
    assert graph2.__contains__(new_predicate_description)
    assert graph2.__contains__(new_predicate_label)
