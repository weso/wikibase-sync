""" Module to provide mappings between different datatypes in XSD and their wdi representation. """

import datetime

from functools import partial
from typing import Union

from wikidataintegrator import wdi_core

from .uri_constants import ASIO_BASE, GEO_BASE, XSD_BASE

def create_geo_coordinate_from(content: str, **kwargs) -> wdi_core.WDGlobeCoordinate:
    """ Create a WDGlobecoordinate object from the point representation in a str. """
    latitude, longitude = content[5:].strip('()').split(" ")
    precision = max(latitude[::-1].find('.'), longitude[::-1].find('.'))
    return wdi_core.WDGlobeCoordinate(float(latitude), float(longitude), precision, **kwargs)

def create_wdquantity(content, upper_bound=None, lower_bound=None, **kwargs) -> wdi_core.WDQuantity:
    """ Create a WDQantity object from a number value and its bounds. """
    return wdi_core.WDQuantity(content, upper_bound=upper_bound, lower_bound=lower_bound, **kwargs)

def create_wditemid_from_bool(content, **kwargs):
    # TODO: create a True and False Item automatically and point them to the wikibase item
    # if content:
    #     item_id = WikibaseAdapter.get_or_create_truth_item()
    # else:
    #     item_id = WikibaseAdapter.get_or_create_false_item()
    # return wdi_core.WDItemID(value=item_id, **kwargs)
    raise NotImplementedError("Support for boolean datatypes is not implemented yet.")

def create_wdstring(content: str, **kwargs) -> wdi_core.WDString:
    """ Create a WDString object from a given string. """
    return wdi_core.WDString(value=content, **kwargs)

def create_wdtime(content: Union[datetime.date, datetime.datetime, datetime.time],
                  **kwargs) -> wdi_core.WDTime:
    """ Create a WDTime object from a given datetime object. """
    return wdi_core.WDTime(content.strftime("+%Y-%m-%dT%H:%M:%SZ"), precision=11, **kwargs)

# Creates a wdi object from the given datatype
datatype2wdiobject = {
    f"{GEO_BASE}wktLiteral": create_geo_coordinate_from,
    f"{XSD_BASE}boolean": create_wditemid_from_bool,
    f"{XSD_BASE}date": create_wdtime,
    f"{XSD_BASE}dateTime": create_wdtime,
    f"{XSD_BASE}decimal": create_wdquantity,
    f"{XSD_BASE}double": create_wdquantity,
    f"{XSD_BASE}int": create_wdquantity,
    f"{XSD_BASE}integer": create_wdquantity,
    f"{XSD_BASE}long": create_wdquantity,
    f"{XSD_BASE}negativeInteger": partial(create_wdquantity, upper_bound=0),
    f"{XSD_BASE}nonNegativeInteger": partial(create_wdquantity, lower_bound=0),
    f"{XSD_BASE}normalizedString": create_wdstring,
    f"{XSD_BASE}positiveInteger": partial(create_wdquantity, lower_bound=1),
    f"{XSD_BASE}short": create_wdquantity,
    f"{XSD_BASE}string": create_wdstring,
    f"{XSD_BASE}time": create_wdtime,
    f"{XSD_BASE}token": create_wdstring
}

# Converts a datatype to a wdi DTYPE string
datatype2wdidtype = {
    f"{ASIO_BASE}item": 'wikibase-item',
    f"{ASIO_BASE}property": 'wikibase-property',
    f"{GEO_BASE}wktLiteral": 'globe-coordinate',
    f"{XSD_BASE}boolean": 'wikibase-item',
    f"{XSD_BASE}date": 'time',
    f"{XSD_BASE}dateTime": 'time',
    f"{XSD_BASE}decimal": 'quantity',
    f"{XSD_BASE}double": 'quantity',
    f"{XSD_BASE}int": 'quantity',
    f"{XSD_BASE}integer": 'quantity',
    f"{XSD_BASE}long": 'quantity',
    f"{XSD_BASE}negativeInteger": 'quantity',
    f"{XSD_BASE}nonNegativeInteger": 'quantity',
    f"{XSD_BASE}normalizedString": 'string',
    f"{XSD_BASE}positiveInteger": 'quantity',
    f"{XSD_BASE}short": 'quantity',
    f"{XSD_BASE}time": 'time',
    f"{XSD_BASE}token": 'string',
    f"{XSD_BASE}string": 'string',
}
