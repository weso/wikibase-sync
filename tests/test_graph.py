from .common import load_graph_from
from rdflib import URIRef

graph = load_graph_from("simple.ttl")

triple_1 = ((URIRef('http://www.purl.org/hercules/asio/core#AdministrativePersonnel'),
             URIRef('http://www.w3.org/2002/07/owl#disjointWith'),
             URIRef('http://www.purl.org/hercules/asio/core#ResearchPersonnel')))

triple_2 = ((URIRef('http://www.purl.org/hercules/asio/core#AdministrativePersonnel'),
             URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
             URIRef('http://www.purl.org/hercules/asio/core#HumanResource')))

triple_3 = ((URIRef('http://www.purl.org/hercules/asio/core#AdministrativePersonnel'),
             URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
             URIRef('http://www.w3.org/2002/07/owl#Class')))

triple_4_non_existent = ((URIRef('http://www.purl.org/hercules/asio/core#capital'),
                          URIRef('http://www.w3.org/2002/07/owl#disjointWith'),
                          URIRef('http://www.purl.org/hercules/asio/core#ResearchPersonnel')))


def test_correct_graph():
    assert len(graph) == 3
    assert graph.__contains__(triple_1)
    assert graph.__contains__(triple_2)
    assert graph.__contains__(triple_3)
    assert not graph.__contains__(triple_4_non_existent)
