from .common import MEDIAWIKI_API_URL
from rdflib import URIRef, Graph, Literal
from rdfsync.wb2rdf.conversion import Converter

graph = Graph()
graph.parse("tests/data/synchronization/uld.ttl", format='ttl')
converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph)
wikibase_id_1 = 'Q4'  # human resource
wikibase_id_2 = 'Q11'  # country
wikibase_id_3 = 'Q12'  # student
# stay the same
subject_1_label = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                    URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                    Literal('HumanResource', lang='en')))
# stay the same
subject_1_comment = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                      URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                      Literal('hihi', lang='en')))

# will be deleted
subject_1_old_comment = ((URIRef('http://www.purl.org/hercules/asio/core#HumanResource'),
                          URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                          Literal('borrame', lang='es')))

# will be deleted
subject_2_old_label = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                        URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                        Literal('país', lang='es')))

subject_2_same_label = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                         URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                         Literal('country', lang='en')))

# updated
subject_2_old_description = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                              URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                              Literal('This will be updated', lang='en')))

# updated
subject_2_new_description = ((URIRef('http://www.purl.org/hercules/asio/core#country'),
                              URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                              Literal(
                                  'This property indicates the nationality of a resource. '
                                  'The domain is not set so unpredicted resources within the ontology '
                                  'could be attached to countries.', lang='en')))

subject_3_old_triple_1 = ((URIRef('http://www.purl.org/hercules/asio/core#student'),
                           URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                           URIRef('http://www.w3.org/2002/07/owl#Class')))

subject_3_old_triple_2 = ((URIRef('http://www.purl.org/hercules/asio/core#student'),
                           URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                           URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))

subject_3_old_comment = ((URIRef('http://www.purl.org/hercules/asio/core#student'),
                          URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
                          Literal('This will be deleted', lang='en')))

subject_3_label = ((URIRef('http://www.purl.org/hercules/asio/core#student'),
                    URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
                    Literal('student', lang='en')))


def test_update_labels_and_descriptions():
    assert not graph.__contains__(subject_2_new_description)
    assert graph.__contains__(subject_1_label)
    assert graph.__contains__(subject_1_comment)
    assert graph.__contains__(subject_1_old_comment)
    assert graph.__contains__(subject_2_old_label)
    assert graph.__contains__(subject_2_same_label)
    assert graph.__contains__(subject_2_old_description)

    converter.execute_synchronization(wb_id=wikibase_id_1)
    converter.execute_synchronization(wb_id=wikibase_id_2)

    assert graph.__contains__(subject_2_new_description)
    assert not graph.__contains__(subject_2_old_description)  # updated
    assert not graph.__contains__(subject_1_old_comment)  # deleted
    assert graph.__contains__(subject_2_same_label)  # same
    assert not graph.__contains__(subject_2_old_label)  # deleted
    assert graph.__contains__(subject_1_label)
    assert graph.__contains__(subject_1_comment)


def test_no_labels_or_descriptions():
    graph = Graph()
    graph.parse("tests/data/synchronization/uld2.ttl", format='ttl')
    assert not graph.__contains__(subject_1_label)  # non existent
    assert graph.__contains__(subject_3_old_comment)
    assert graph.__contains__(subject_3_label)
    assert graph.__contains__(subject_3_old_triple_1)
    assert graph.__contains__(subject_3_old_triple_2)
    assert len(graph) == 4

    converter2 = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl', graph=graph)
    converter2.execute_synchronization(wb_id=wikibase_id_3)

    assert not graph.__contains__(subject_1_label)  # non existent
    assert not graph.__contains__(subject_3_old_comment)  # deleted
    assert graph.__contains__(subject_3_label)
    assert not graph.__contains__(subject_3_old_triple_1)  # deleted
    assert not graph.__contains__(subject_3_old_triple_2)  # deleted
