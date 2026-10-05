import pytest
from rest_framework.exceptions import ValidationError, APIException
from apps.core.exceptions import custom_exception_handler


class MockContext:
    pass


def test_custom_exception_handler_with_dict_detail():
    exc = ValidationError({'detail': 'Direct string error'})
    response = custom_exception_handler(exc, {})
    assert response is not None
    assert response.data['detail'] == 'Direct string error'
    assert response.data['code'] == 'invalid'


def test_custom_exception_handler_with_field_errors():
    exc = ValidationError({'username': ['This field is required.'], 'email': ['Enter a valid email.']})
    response = custom_exception_handler(exc, {})
    assert response is not None
    assert 'username: This field is required.' in response.data['detail']
    assert 'email: Enter a valid email.' in response.data['detail']
    assert 'errors' in response.data


def test_custom_exception_handler_with_list_errors():
    exc = ValidationError(['First error in list', 'Second error in list'])
    response = custom_exception_handler(exc, {})
    assert response is not None
    assert isinstance(response.data['detail'], str)
    assert response.data['detail'] == 'First error in list; Second error in list'
    assert response.data['errors'] == ['First error in list', 'Second error in list']
