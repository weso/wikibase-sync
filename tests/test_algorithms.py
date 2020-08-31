import pytest

from rdflib.namespace import XSD

from wbsync.synchronization import AdditionOperation, RemovalOperation, \
                                          GraphDiffSyncAlgorithm, NaiveSyncAlgorithm, \
                                          RDFSyncAlgorithm
from wbsync.triplestore import LiteralElement, URIElement
from wbsync.util.uri_constants import RDFS_COMMENT, RDFS_LABEL, RDFS_SUBCLASSOF, \
                                             RDF_TYPE, OWL_CLASS, OWL_DISJOINT_WITH

from .common import load_file_from

SOURCE_FILE = 'source.ttl'
TARGET_FILE = 'target.ttl'

ASIO_PREFIX = 'http://www.asio.es/asioontologies/asio#'
EX_PREFIX = 'http://www.semanticweb.org/spitxa/ontologies/2020/1/asio-human-resource#'


@pytest.fixture(scope='module')
def input():
    return load_file_from(SOURCE_FILE, TARGET_FILE)


class TestNaiveSyncAlgorithm:
    @pytest.fixture(scope='class')
    def algorithm(self):
        return NaiveSyncAlgorithm()

    def test_not_implemented(self, algorithm, input):
        with pytest.raises(NotImplementedError) as excpt:
            algorithm.do_algorithm(input[0], input[1])
        assert 'has not been implemented yet' in str(excpt.value)


class TestRDFSyncAlgorithm:
    @pytest.fixture(scope='class')
    def algorithm(self):
        return RDFSyncAlgorithm()

    def test_not_implemented(self, algorithm, input):
        with pytest.raises(NotImplementedError) as excpt:
            algorithm.do_algorithm(input[0], input[1])
        assert 'has not been implemented yet' in str(excpt.value)


class TestGraphSyncAlgorithm:
    @pytest.fixture(scope='class')
    def algorithm(self):
        return GraphDiffSyncAlgorithm()

    def test_basic(self, algorithm, input):
        operations = algorithm.do_algorithm(input[0], input[1])

        administrative_personnel = EX_PREFIX + 'AdministrativePersonnel'
        changed_personnel = EX_PREFIX + 'ChangedPersonnel'
        human_resource = ASIO_PREFIX + 'HumanResource'
        research_personnel = EX_PREFIX + 'ResearchPersonnel'
        technical_personnel = ASIO_PREFIX + 'TechnicalPersonnel'

        addition_ops = [
            AdditionOperation(URIElement(administrative_personnel),
                              URIElement(OWL_DISJOINT_WITH),
                              URIElement(changed_personnel)),
            AdditionOperation(URIElement(changed_personnel),
                              URIElement(RDF_TYPE),
                              URIElement(OWL_CLASS)),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDF_TYPE),
                              URIElement(OWL_CLASS)),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_SUBCLASSOF),
                              URIElement(human_resource)),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_COMMENT),
                              LiteralElement('Personnel devoted to technical suport.', lang='en')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Personal tècnic', lang='ca-ad')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Personal tècnic', lang='ca-es')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Personal técnico', lang='es')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Personnel technique', lang='fr')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Pessoal técnico', lang='pt')),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement(12, datatype=XSD.integer)),
            AdditionOperation(URIElement(technical_personnel),
                              URIElement(RDFS_LABEL),
                              LiteralElement('Technical personnel', lang='en'))
        ]
        removal_ops = [
            RemovalOperation(URIElement(administrative_personnel),
                             URIElement(OWL_DISJOINT_WITH),
                             URIElement(research_personnel)),
            RemovalOperation(URIElement(research_personnel),
                             URIElement(RDF_TYPE),
                             URIElement(OWL_CLASS)),
            RemovalOperation(URIElement(research_personnel),
                             URIElement(RDFS_SUBCLASSOF),
                             URIElement(EX_PREFIX + 'HumanResource'))
        ]
        expected = addition_ops + removal_ops

        assert len(operations) == len(expected)
        _assert_lists_have_same_elements(expected, operations)

        for op in operations:
            triple = op._triple_info
            if isinstance(op, AdditionOperation):
                assert triple.isAdded
            elif isinstance(op, RemovalOperation):
                assert not triple.isAdded
            else:
                assert False, "Invalid operation type detected"


def _assert_lists_have_same_elements(expected, result):
    for el in result:
        assert el in expected
    for el in expected:
        assert el in result
