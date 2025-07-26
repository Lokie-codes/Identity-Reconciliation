import pytest
from rest_framework.exceptions import ValidationError
from api.serializers import RequestSerializer, ContactSerializer, ResponseSerializer

# Tests for RequestSerializer

def test_request_serializer_valid_email():
    data = {"email": "test@example.com"}
    serializer = RequestSerializer(data=data)
    assert serializer.is_valid()

def test_request_serializer_valid_phone():
    data = {"phoneNumber": "1234567890"}
    serializer = RequestSerializer(data=data)
    assert serializer.is_valid()

def test_request_serializer_valid_both():
    data = {"email": "test@example.com", "phoneNumber": "1234567890"}
    serializer = RequestSerializer(data=data)
    assert serializer.is_valid()

def test_request_serializer_invalid_none():
    data = {}
    serializer = RequestSerializer(data=data)
    assert not serializer.is_valid()
    assert "At least one of 'email' or 'phoneNumber' must be provided." in str(serializer.errors)

# Tests for ContactSerializer

def test_contact_serializer_valid_primary_id():
    data = {"primaryContactId": 1}
    serializer = ContactSerializer(data=data)
    assert serializer.is_valid()

def test_contact_serializer_valid_emails():
    data = {"emails": ["test@example.com"]}
    serializer = ContactSerializer(data=data)
    assert serializer.is_valid()

def test_contact_serializer_valid_phone_numbers():
    data = {"phoneNumbers": ["1234567890"]}
    serializer = ContactSerializer(data=data)
    assert serializer.is_valid()

def test_contact_serializer_valid_all_fields():
    data = {
        "primaryContactId": 1,
        "emails": ["test@example.com"],
        "phoneNumbers": ["1234567890"],
        "secondaryContactIds": [2, 3]
    }
    serializer = ContactSerializer(data=data)
    assert serializer.is_valid()

def test_contact_serializer_invalid_none():
    data = {}
    serializer = ContactSerializer(data=data)
    assert not serializer.is_valid()
    assert "At least one of 'primaryContactId', 'emails', or 'phoneNumbers' must be provided." in str(serializer.errors)

# Tests for ResponseSerializer

def test_response_serializer_valid_contact():
    data = {
        "contact": {
            "primaryContactId": 1,
            "emails": ["test@example.com"],
            "phoneNumbers": ["1234567890"],
            "secondaryContactIds": [2]
        }
    }
    serializer = ResponseSerializer(data=data)
    assert serializer.is_valid()

def test_response_serializer_invalid_contact_none():
    data = {"contact": {}}
    serializer = ResponseSerializer(data=data)
    assert not serializer.is_valid()
    # Convert ErrorDetail to string for comparison
    error_list = serializer.errors["contact"]["non_field_errors"]
    assert any(
        "At least one of 'primaryContactId', 'emails', or 'phoneNumbers' must be provided." in str(err)
        for err in error_list
    )