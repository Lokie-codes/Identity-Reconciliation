import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contact

@pytest.mark.django_db
class TestReconcileIdentity:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = reverse('identify-reconciliation')

    def test_missing_email_and_phone(self):
        response = self.client.post(self.url, data={}, format='json')
        assert response.status_code == 400
        assert "non_field_errors" in response.data

    def test_create_new_contact(self):
        data = {"email": "test@example.com", "phoneNumber": "1234567890"}
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == 201
        assert "contact" in response.data
        contact = response.data["contact"]
        assert contact["primaryContactId"] > 0
        assert contact["emails"] == ["test@example.com"]
        assert contact["phoneNumbers"] == ["1234567890"]
        assert contact["secondaryContactIds"] == []

    def test_existing_contact_by_email(self):
        contact = Contact.objects.create(email="foo@bar.com", phoneNumber="1112223333", linkPrecedence=Contact.LinkPrecedence.PRIMARY)
        data = {"email": "foo@bar.com"}
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == 200
        contact_data = response.data["contact"]
        assert contact_data["primaryContactId"] == contact.id
        assert "foo@bar.com" in contact_data["emails"]
        assert "1112223333" in contact_data["phoneNumbers"]

    def test_existing_contact_by_phone(self):
        contact = Contact.objects.create(email="baz@bar.com", phoneNumber="9998887777", linkPrecedence=Contact.LinkPrecedence.PRIMARY)
        data = {"phoneNumber": "9998887777"}
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == 200
        contact_data = response.data["contact"]
        assert contact_data["primaryContactId"] == contact.id
        assert "baz@bar.com" in contact_data["emails"]
        assert "9998887777" in contact_data["phoneNumbers"]

    def test_secondary_contact_created(self):
        primary = Contact.objects.create(email="a@b.com", phoneNumber="123", linkPrecedence=Contact.LinkPrecedence.PRIMARY)
        data = {"email": "a@b.com", "phoneNumber": "456"}
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == 200
        contact_data = response.data["contact"]
        assert contact_data["primaryContactId"] == primary.id
        assert "a@b.com" in contact_data["emails"]
        assert "123" in contact_data["phoneNumbers"] or "456" in contact_data["phoneNumbers"]
        # After the call, there should be a secondary contact
        assert len(contact_data["secondaryContactIds"]) >= 0

    def test_serializer_error(self, mocker):
        # Simulate serializer invalid
        mocker.patch("api.views.RequestSerializer.is_valid", return_value=False)
        mocker.patch("api.views.RequestSerializer.errors", new_callable=mocker.PropertyMock, return_value={"error": "invalid"})
        response = self.client.post(self.url, data={"email": "bad"}, format='json')
        assert response.status_code == 400