import pytest
from api.models import Contact

@pytest.mark.django_db
def test_contact_str_primary():
    contact = Contact.objects.create(
        phoneNumber="1234567890",
        email="test@example.com",
        linkedId=None,
        linkPrecedence=Contact.LinkPrecedence.PRIMARY
    )
    expected = (
        f"Contact(id={contact.id}, phoneNumber=1234567890, email=test@example.com "
        f"linkedId=None, linkPrecedence=primary)"
    )
    assert str(contact) == expected

@pytest.mark.django_db
def test_contact_str_secondary_with_linkedId():
    contact = Contact.objects.create(
        phoneNumber="0987654321",
        email="foo@bar.com",
        linkedId=1,
        linkPrecedence=Contact.LinkPrecedence.SECONDARY
    )
    expected = (
        f"Contact(id={contact.id}, phoneNumber=0987654321, email=foo@bar.com "
        f"linkedId=1, linkPrecedence=secondary)"
    )
    assert str(contact) == expected

@pytest.mark.django_db
def test_contact_str_null_fields():
    contact = Contact.objects.create(
        phoneNumber=None,
        email=None,
        linkedId=None,
        linkPrecedence=Contact.LinkPrecedence.PRIMARY
    )
    expected = (
        f"Contact(id={contact.id}, phoneNumber=None, email=None "
        f"linkedId=None, linkPrecedence=primary)"
    )
    assert str(contact) == expected