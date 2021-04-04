""" Module to get the names of each subject, predicate, object of a triple individually"""
from .errors import StringValidationError
import re
from dateutil.parser import parse
import time

valid_url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_triple_subject_str(subject):
    """

    Parameters
    ----------
    subject: the related link or the full namespace of the subject

    Returns
    -------
    the name/label of subject without link
    """
    if not subject:
        return ''
    if re.match(valid_url_regex, subject) is not None:
        if '#' in subject:
            object_to_string = str(subject).rsplit("/", 1)[-1]
            obj_name = object_to_string.rpartition("#")[2]
            return obj_name
        else:
            subject.rsplit('/', 1)
            return subject.rsplit('/', 1)[-1]
    else:
        raise StringValidationError()


def get_triple_predicate_str(predicate):
    """

    Parameters
    ----------
    predicate: the related link or the full namespace of the predicate

    Returns
    -------
    the name/label of predicate without link
    """
    if not predicate:
        return ''
    if re.match(valid_url_regex, predicate) is not None:
        if '#' in predicate:
            object_to_string = str(predicate).rsplit("/", 1)[-1]
            obj_name = object_to_string.rpartition("#")[2]
            return obj_name
        else:
            predicate.rsplit('/', 1)
            return predicate.rsplit('/', 1)[-1]

    else:
        raise StringValidationError()


def get_namespace(link_string):
    """

    Parameters
    ----------
    link_string: the related link or the full namespace/link

    Returns
    -------
    the link without the final word.
    example : input: http://www.w3.org/2002/07/owl#Class
              returns: http://www.w3.org/2002/07/owl#
    """
    if re.match(valid_url_regex, link_string) is not None:
        if '#' in link_string:
            i = link_string.index('#')
            return link_string[:i + len('#')]
        else:
            link_string.rsplit('/', 1)
            return link_string.rsplit('/', 1)[0] + '/'
    else:
        raise StringValidationError()


def is_date(string, fuzzy=False):
    """

    Parameters
    ----------
    string: str, string to check for date
    fuzzy: bool, ignore unknown tokens in string if True

    Returns
    -------
    true if a string is a correct date format
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        raise ValueError("invalid date format")


def is_time_format(string_input):
    """

    Parameters
    ----------
    string_input: string of a date

    Returns
    -------
    true if a string has a correct time format HH:MM
    """
    try:
        time.strptime(string_input, '%H:%M')
        return True
    except ValueError:
        raise ValueError("invalid time format")
