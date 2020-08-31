from typing import List

from . import BaseSyncAlgorithm, NaiveSyncAlgorithm, SyncOperation
from ..triplestore import URIElement
from ..util.uri_constants import ASIO_BASE, XSD_BASE

import ontospy

class OntologySynchronizer():
    """ Processes information from a GitHub push event.

    This class uses a syncrhonization algorithm to return the list of operations
    that need to be execute to synchronize a GitFile and a given triplestore.

    Parameters
    ----------
    algoritm : :obj:`BaseSyncAlgorithm`
        Algorithm that conforms to the BaseSyncAlgorithm interface.
    """

    def __init__(self, algorithm: BaseSyncAlgorithm):
        self._algorithm = algorithm if algorithm is not None else NaiveSyncAlgorithm()

    def synchronize(self, source_content: str, target_content: str) -> List[SyncOperation]:
        """ Execute the algorithm to obtain the list of operations to execute.

        Parameters
        ----------
        source_content : str
            String containing the original RDF content before any modification.

        target_content : str
            String containing the final RDF content after the modifications.

        Returns
        -------
        list of :obj:`SyncOperation`
            List of operations that need to be executed to synchronize the file
            with the triplestore.
        """
        ops = self._algorithm.do_algorithm(source_content, target_content)
        filtered_ops = _filter_invalid_ops(ops)
        self._annotate_triples(filtered_ops, source_content, target_content)
        return filtered_ops

    def _annotate_triples(self, ops: List[SyncOperation], source_content: str, target_content: str):
        source_model = ontospy.Ontospy(data=source_content, rdf_format='ttl')
        target_model = ontospy.Ontospy(data=target_content, rdf_format='ttl')
        all_urielements = _extract_uris_from(ops)
        _annotate_uris_etype(all_urielements, source_model, target_model)
        _annotate_datatype_props(all_urielements, source_model, target_model)
        _annotate_object_props(all_urielements, source_model, target_model)

def _annotate_datatype_props(all_urielements, source_model, target_model):
    datatype_properties = source_model.all_properties_datatype + \
                          target_model.all_properties_datatype
    for urielement in all_urielements:
        for prop in datatype_properties:
            if urielement == str(prop.uri):
                if len(prop.ranges) > 0:
                    urielement.proptype = str(prop.ranges[0].uri)
                else:
                    # default type for datatype properties without range
                    urielement.proptype = f'{XSD_BASE}string'

def _annotate_object_props(all_urielements: List[URIElement], source_model, target_model):
    object_properties = source_model.all_properties_object + target_model.all_properties_object
    for urielement in all_urielements:
        for prop in object_properties:
            if urielement == str(prop.uri):
                if len(prop.ranges) > 0:
                    prop_range = prop.ranges[0]
                    urielement.proptype = f'{ASIO_BASE}property' \
                        if isinstance(prop_range, ontospy.core.entities.OntoProperty) \
                        else f'{ASIO_BASE}item'
                else:
                    # default type for object properties without range
                    urielement.proptype = f'{ASIO_BASE}item'

def _annotate_uris_etype(all_urielements: List[URIElement], source_model, target_model):
    properties = source_model.all_properties + target_model.all_properties
    properties_uris = list(map(lambda x: str(x.uri), properties))
    for urielement in all_urielements:
        if urielement in properties_uris:
            urielement.etype = 'property'

def _extract_uris_from(ops: List[SyncOperation]) -> List[URIElement]:
    return [el for op in ops
            for el in op._triple_info
            if el.is_uri]

def _filter_invalid_ops(ops: List[SyncOperation]) -> List[SyncOperation]:
    return list(filter(lambda op: op._triple_info.subject is not None and
                                  op._triple_info.predicate is not None and
                                  op._triple_info.object is not None, ops))
