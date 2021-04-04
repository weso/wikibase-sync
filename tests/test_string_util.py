import pytest
from rdfsync.util.string_util import get_namespace, get_triple_predicate_str, get_triple_subject_str, \
    StringValidationError

related_link_subject = "http://www.w3.org/2002/07/owl#Class"
related_link_object = "http://www.w3.org/2004/02/skos/core#Concept"
related_link_predicate = "http://www.purl.org/hercules/asio/core#AdministrativePersonnel"
namespace_with_star = "http://www.w3.org/2004/02/skos/core#Concept"
namespace_with_slash = "http://www.w3.org/2004/02/skos/core/Concept"
invalid_link = "http://google"


def test_triple_subject_name():
    value = get_triple_subject_str(related_link_subject)
    assert value == 'Class'
    value = get_triple_subject_str(namespace_with_slash)
    assert value == 'Concept'
    assert get_triple_subject_str("") == ''
    with pytest.raises(StringValidationError):
        get_triple_subject_str("not working")


def test_triple_predicate_name():
    value = get_triple_predicate_str(related_link_predicate)
    assert value == 'AdministrativePersonnel'
    value = get_triple_predicate_str(namespace_with_slash)
    assert value == 'Concept'
    assert get_triple_predicate_str("") == ''
    with pytest.raises(StringValidationError):
        get_triple_predicate_str("not working")


def test_namespace_name():
    value = get_namespace(namespace_with_slash)
    assert str(value) == str("http://www.w3.org/2004/02/skos/core/")
    value = get_namespace(namespace_with_star)
    assert str(value) == str("http://www.w3.org/2004/02/skos/core#")
    with pytest.raises(StringValidationError):
        get_namespace("not working")
    with pytest.raises(StringValidationError):
        get_namespace(invalid_link)
