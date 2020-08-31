import logging

from abc import abstractmethod, ABC
from typing import Type, Union

from rdflib.term import BNode, Literal, URIRef
from wikidataintegrator.wdi_core import WDBaseDataType, WDItemID, WDMonolingualText, \
                                        WDProperty, WDString


from ..util.error import InvalidArgumentError
from ..util.mappings import datatype2wdidtype, datatype2wdiobject
from ..util.uri_constants import ASIO_BASE

logger = logging.getLogger(__name__)

class TripleElement(ABC):
    """ Element of a semantic triple.

    This abstract class represents the common behaviour exposed by an element
    of a semantic triple.
    """

    @classmethod
    def from_rdflib(cls, rdflib_element):
        """ Create a TripleElement from a rdflib term.

        Parameters
        ----------
        rdflib_element : :obj:`rdflib.term`
            Rdflib element used to create the TripleElement.

        Returns
        -------
        :obj:`TripleElement`
            TripleElement equivalent to the rdflib term.
        """
        elmnt_type = type(rdflib_element)
        res = None
        if elmnt_type == URIRef:
            res = URIElement(str(rdflib_element))
        elif elmnt_type == Literal:
            res = LiteralElement(rdflib_element.value, rdflib_element.datatype,
                                 rdflib_element.language)
        elif elmnt_type == BNode:
            res = AnonymousElement(str(rdflib_element))
        return res

    @abstractmethod
    def to_wdi_datatype(self, **kwargs):
        """ Return a wdi instance representing the current element.

        Returns
        -------
        :obj:`wikidataintegrator.wdi_core.WDBaseDataType`
            Instance of a wdi datatype that represents this TripeElement.
        """

    def is_uri(self):
        return False

    def is_blank(self):
        return False

    def is_literal(self):
        return False

class AnonymousElement(TripleElement):
    """ TripleElement class that represents blank nodes from a triple.

    Parameters
    ----------
    uid : str
        Generated uid of the element.
    """
    def __init__(self, uid: str, prefix: str = ASIO_BASE):
        self.uid = uid
        self.prefix = prefix
        self.etype = 'item'
        self.id = None

    @property
    def uri(self) -> str:
        return f"{self.prefix}/genid/{self.uid}"

    @property
    def wdi_class(self) -> Type[WDItemID]:
        """ Returns the wikidataintegrator class of the element.
        """
        return WDItemID

    @property
    def wdi_dtype(self) -> str:
        """ Returns the wikidataintegrator DTYPE of this element.
        """
        return self.wdi_class.DTYPE

    @property
    def wdi_proptype(self) -> str:
        return None

    def to_wdi_datatype(self, **kwargs) -> WDItemID:
        return self.wdi_class(value=self.id, **kwargs)

    def is_blank(self):
        return True

    def __eq__(self, val):
        return self.uri == val

    def __iter__(self):
        return self.uri.__iter__()

    def __str__(self):
        return f"AnonymousElement: {self.uri}"


class URIElement(TripleElement):
    """ TripleElement class that represents URIs from a triple.

    Parameters
    ----------
    uri : str
        URI of the element.
    """

    DEFAULT_PROPTYPE = 'string'
    VALID_ETYPES = ['item', 'property']

    def __init__(self, uri: str, etype='item', proptype=None):
        self.uri = uri
        self.etype = etype
        self.proptype = proptype
        self.id = None

    @property
    def etype(self) -> str:
        """ Get the entity type of this element.

        Returns
        -------
        str
            'item' if the element corresponds to a wikibase item and 'property'
            if it corresponds to a wikibase property.
        """
        return self._etype

    @property
    def wdi_proptype(self) -> str:
        """ Returns the range of this URI as a wdi property string.

        str
            The range of this URI, corresponding to a DTYPE of the property datatypes
            allowed in wikibase.
        """
        if self.etype == 'item' or self.proptype is None:
            return None

        if self.proptype not in datatype2wdidtype:
            logger.warning("Property type %s is not supported, returning None", self.proptype)
            return None
        return datatype2wdidtype[self.proptype]

    @etype.setter
    def etype(self, new_val: str) -> str:
        if new_val not in self.VALID_ETYPES:
            raise InvalidArgumentError('Invalid etype received, valid values are: ',
                                       self.VALID_ETYPES)
        self._etype = new_val
        return self._etype

    @property
    def wdi_class(self) -> Union[Type[WDItemID], Type[WDProperty]]:
        """ Returns the wikidataintegrator class of the element.
        """
        assert self.etype in self.VALID_ETYPES
        return WDItemID if self.etype == 'item' else WDProperty

    @property
    def wdi_dtype(self) -> str:
        """ Returns the wikidataintegrator DTYPE of this element.
        """
        return self.wdi_class.DTYPE

    def to_wdi_datatype(self, **kwargs) -> Union[WDItemID, WDProperty]:
        return self.wdi_class(value=self.id, **kwargs)

    def is_uri(self):
        return True

    def __eq__(self, val):
        return self.uri == val

    def __hash__(self):
        return hash(self.uri)

    def __iter__(self):
        return self.uri.__iter__()

    def __str__(self):
        return f"URIElement: {self.uri} - Type: {self.etype}"


class LiteralElement(TripleElement):
    """ TripleElement class that represents a literal from a triple.

    Parameters
    ----------
    content : any
        Content of the literal.
    datatype : str
        URI of the xsd schema of the literal's datatype.
    lang : str
        If the literal is a language tagged string, language of it.

    Raises
    ------
    InvalidArgumentError
        If both the datatype and lang parameters are provided.
    """

    def __init__(self, content, datatype=None, lang=None):
        self.content = content
        if datatype and lang:
            raise InvalidArgumentError("Both datatype and language can't be set.")
        self.datatype = datatype
        self.lang = lang

    @property
    def wdi_class(self) -> Type[WDBaseDataType]:
        if self.lang:
            return WDMonolingualText
        elif self.datatype:
            return self._datatype_to_wdiobject(prop_nr=-1).__class__
        else:
            return WDString

    @property
    def wdi_dtype(self) -> str:
        return self.wdi_class.DTYPE

    def to_wdi_datatype(self, **kwargs) -> WDBaseDataType:
        if self.lang:
            return self.wdi_class(value=self.content, language=self.lang, **kwargs)
        elif self.datatype:
            return self._datatype_to_wdiobject(**kwargs)
        else:
            return self.wdi_class(value=self.content, **kwargs)

    def is_literal(self):
        return True

    def _datatype_to_wdiobject(self, **kwargs) -> WDBaseDataType:
        if str(self.datatype) not in datatype2wdiobject:
            logger.warning("Datatype %s is not supported, defaulting to string...", self.datatype)
            self.content = "" if self.content is None else self.content
            return WDString(value=self.content, **kwargs)
        return datatype2wdiobject[str(self.datatype)](self.content, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, LiteralElement):
            return False
        return self.content == other.content and self.lang == other.lang \
               and self.datatype == other.datatype

    def __str__(self):
        res = [f"LiteralElement: {self.content}"]
        if self.lang:
            res.append(f" - Language: {self.lang}")
        if self.datatype:
            res.append(f" - DataType: {self.datatype}")
        return ''.join(res)


class TripleInfo():
    """ Encapsulate the elements of a semantic triple.

    Parameters
    ----------
    sub : :obj:`TripleElement`
        Subject of the triple.
    pred : :obj:`TripleElement`
        Predicate of the triple.
    obj : :obj:`TripleElement`
        Object of the triple.
    """

    def __init__(self, sub: TripleElement, pred: TripleElement, obj: TripleElement,
                 isAdded=True):
        self.subject = sub
        self.predicate = pred
        self.object = obj
        self.isAdded = isAdded

    @classmethod
    def from_rdflib(cls, rdflib_triple, isAdded=True):
        subject = TripleElement.from_rdflib(rdflib_triple[0])
        predicate = TripleElement.from_rdflib(rdflib_triple[1])
        objct = TripleElement.from_rdflib(rdflib_triple[2])
        return TripleInfo(subject, predicate, objct, isAdded)

    @property
    def content(self):
        """ Return each element of the triple in a tuple.

        Returns
        -------
        tuple
            Tuple of three elements, containing the subject, predicate and object of the triple.
        """
        return (self.subject, self.predicate, self.object)

    def __eq__(self, other):
        if not isinstance(other, TripleInfo):
            return False

        return self.subject == other.subject and self.predicate == other.predicate \
            and self.object == other.object

    def __iter__(self):
        return self.content.__iter__()

    def __str__(self):
        return f"{self.subject} - {self.predicate} - {self.object}"
