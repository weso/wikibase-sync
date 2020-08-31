from abc import ABC, abstractmethod

from . import TripleInfo

class ModificationResult():
    def __init__(self, successful: bool, message: str = "", res=""):
        self.successful = successful
        self.message = message
        self.result = res

class TripleStoreManager(ABC):
    """ Base class to execute operations on a triplestore.

    The methods of this class must be implemented by each specific triplestore
    adapter to allow the execution of SyncOperations on the triplestore.
    """

    @abstractmethod
    def create_triple(self, triple_info: TripleInfo) -> ModificationResult:
        """ Adds a new triple to the triplestore.

        Parameters
        ----------
        triple_info : :obj:`TripleInfo`
            Triple that will be added to the triple store.

        Returns
        -------
        :obj:`ModificationResult`
            Result of the operation.
        """

    @abstractmethod
    def remove_triple(self, triple_info: TripleInfo) -> ModificationResult:
        """ Remove a triple from the triplestore.

        Parameters
        ----------
        triple_info : :obj:`TripleInfo`
            Triple that needs to be removed from the tripe store.

        Returns
        -------
        :obj:`ModificationResult`
            Result of the operation.
        """
