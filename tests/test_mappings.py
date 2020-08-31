import pytest

from datetime import date, datetime, time

from wikidataintegrator import wdi_core

from wbsync.util.mappings import datatype2wdiobject, datatype2wdidtype
from wbsync.util.uri_constants import GEO_BASE, XSD_BASE

def test_time_mapping():
    time_val = time(4, 24 ,0)
    result = datatype2wdiobject[f"{XSD_BASE}time"](time_val, prop_nr=-1)
    expected = wdi_core.WDTime(time="+1900-01-01T04:24:00Z", prop_nr=-1)
    assert result == expected

def test_date_mappings():
    time_val = date(2000, 11, 30)
    result = datatype2wdiobject[f"{XSD_BASE}time"](time_val, prop_nr=-1)
    expected = wdi_core.WDTime(time="+2000-11-30T00:00:00Z", prop_nr=-1)
    assert result == expected

def test_datetime_mappings():
    time_val = datetime(2000, 11, 30, 11, 30, 00)
    result = datatype2wdiobject[f"{XSD_BASE}time"](time_val, prop_nr=-1)
    expected = wdi_core.WDTime(time="+2000-11-30T11:30:00Z", prop_nr=-1)
    assert result == expected

def test_geocoordinates_mapping():
    result = datatype2wdiobject[f"{GEO_BASE}wktLiteral"]("Point(36.834 2.463)", prop_nr=-1)
    expected = wdi_core.WDGlobeCoordinate(latitude=36.834, longitude=2.463, precision=3, prop_nr=-1)
    assert result == expected

def test_quantity():
    result = datatype2wdiobject[f"{XSD_BASE}integer"](-125, prop_nr=-1)
    expected = wdi_core.WDQuantity(value=-125, prop_nr=-1)
    assert result == expected

def test_quantity_bounds():
    result = datatype2wdiobject[f"{XSD_BASE}positiveInteger"](50, prop_nr=-1)
    expected = wdi_core.WDQuantity(value=50, lower_bound=1, prop_nr=-1)
    assert result == expected

def test_string():
    result = datatype2wdiobject[f"{XSD_BASE}string"]("Hello", prop_nr=-1)
    expected = wdi_core.WDString(value="Hello", prop_nr=-1)
    assert result == expected
