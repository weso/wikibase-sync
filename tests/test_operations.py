from unittest import mock

import pytest

from wbsync.synchronization import AdditionOperation, BatchOperation, RemovalOperation
from wbsync.synchronization.operations import optimize_ops
from wbsync.triplestore import LiteralElement, TripleInfo, URIElement
from wbsync.util.uri_constants import RDFS_LABEL


@pytest.fixture
def mock_triplestore():
    return mock.MagicMock()


@pytest.fixture
def triple():
    subject = URIElement('http://example.org/onto#Person')
    predicate = URIElement(RDFS_LABEL)
    objct = LiteralElement('Persona', 'es')
    return (subject, predicate, objct)


def test_init(triple):
    addition_op = AdditionOperation(*triple)
    assert addition_op._triple_info == TripleInfo(*triple)


def test_str(triple):
    addition_op = AdditionOperation(*triple)
    assert str(addition_op) == f"AdditionOperation: {triple[0]} - {triple[1]} - {triple[2]}"

    removal_op = RemovalOperation(*triple)
    assert str(removal_op) == f"RemovalOperation: {triple[0]} - {triple[1]} - {triple[2]}"

    batch_op = BatchOperation(triple[0], [triple, triple])
    assert str(batch_op) == f"BatchOperation: {triple[0]}\n{triple}\n{triple}"


def test_addition(mock_triplestore, triple):
    addition_op = AdditionOperation(*triple)
    addition_op.execute(mock_triplestore)
    mock_triplestore.create_triple.assert_called_once_with(TripleInfo(*triple))


def test_batch(mock_triplestore, triple):
    triples = [triple] * 3
    batch_op = BatchOperation(triple[0], triples)
    batch_op.execute(mock_triplestore)
    mock_triplestore.batch_update.assert_called_once_with(triple[0], triples)


def test_removal(mock_triplestore, triple):
    removal_op = RemovalOperation(*triple)
    removal_op.execute(mock_triplestore)
    mock_triplestore.remove_triple.assert_called_once_with(TripleInfo(*triple))


def test_optimize_ops(triple):
    triple_b = (URIElement('http://example.org/onto#Singer'), URIElement(RDFS_LABEL),
                LiteralElement('Cantante', 'es'))
    original_ops = [AdditionOperation(*triple), AdditionOperation(*triple_b), RemovalOperation(*triple)]
    result_ops = optimize_ops(original_ops)
    assert len(result_ops) == 2
    for op in result_ops:
        assert isinstance(op, BatchOperation)


def test_two_operations_with_same_triple_are_distinct(triple):
    add = AdditionOperation(*triple)
    remove = RemovalOperation(*triple)
    assert add != remove
