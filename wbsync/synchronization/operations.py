from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List

from ..triplestore import ModificationResult, TripleStoreManager, \
                          TripleElement, TripleInfo


class SyncOperation(ABC):
    @abstractmethod
    def execute(self, triple_store: TripleStoreManager) -> ModificationResult:
        """ Executes the operation in the given triple store.

        Parameters
        ----------
        triple_store : :obj:`TripleStoreManager`
            Instance of triple store manager

        Returns
        -------
        :obj: `ModificationResult`
            Result given by the TripleStoreManager after the modification.

        """


class BasicSyncOperation(SyncOperation):
    """ Base class of all the basic synchronization operations.

    Parameters
    ----------
    sub : TripleElement
        Subject of the triple to be synchronized.
    pred : TripleElement
        Predicate of the triple to be synchronized.
    obj : TripleElement
        Object of the triple to be synchronized.
    """
    def __init__(self, sub: TripleElement, pred: TripleElement, obj: TripleElement):
        pass

    def __str__(self):
        return f"{self._triple_info.subject} - {self._triple_info.predicate} " \
               + f"- {self._triple_info.object}"


class AdditionOperation(BasicSyncOperation):
    def __init__(self, sub: TripleElement, pred: TripleElement, obj: TripleElement):
        self._triple_info = TripleInfo(sub, pred, obj, isAdded=True)

    def execute(self, triple_store: TripleStoreManager) -> ModificationResult:
        return triple_store.create_triple(self._triple_info)

    def __str__(self):
        return "AdditionOperation: " + super(AdditionOperation, self).__str__()

    def __eq__(self, other):
        if not isinstance(other, AdditionOperation):
            return False

        return self._triple_info == other._triple_info


class RemovalOperation(BasicSyncOperation):
    def __init__(self, sub: TripleElement, pred: TripleElement, obj: TripleElement):
        self._triple_info = TripleInfo(sub, pred, obj, isAdded=False)

    def execute(self, triple_store: TripleStoreManager) -> ModificationResult:
        return triple_store.remove_triple(self._triple_info)

    def __str__(self):
        return "RemovalOperation: " + super(RemovalOperation, self).__str__()

    def __eq__(self, other):
        if not isinstance(other, RemovalOperation):
            return False

        return self._triple_info == other._triple_info


class BatchOperation(SyncOperation):
    """ Synchronization operation that performs a batch update on the triplestore

    Parameters
    ----------
    sub : TripleElement
        Common subject of the triples that will be updated.
    triples : list of TripleInfo
        List of triples to be updated at once with the batch update.
    """

    def __init__(self, subject: TripleElement, triples: List[TripleInfo]):
        self.subject = subject
        self.triples = triples

    def execute(self, triple_store: TripleStoreManager) -> ModificationResult:
        return triple_store.batch_update(self.subject, self.triples)

    def __str__(self):
        res = [f"BatchOperation: {self.subject}"]
        for triple in self.triples:
            res.append('\n')
            res.append(str(triple))
        return ''.join(res)


def optimize_ops(ops: List[BasicSyncOperation]) -> List[BatchOperation]:
    """ Convert a list of basic operations into a list of batch operations.

    Parameters
    ----------
    ops: list of BasicSyncOperation
        Input basic operations to be converted.

    Returns
    -------
    list of BatchOperations
        Final list of batch operations to be executed.
    """
    subject_to_triples = defaultdict(list)
    for op in ops:
        triple_info = op._triple_info
        subject_to_triples[triple_info.subject].append(triple_info)

    return [BatchOperation(subject, triples)
            for subject, triples in subject_to_triples.items()]
