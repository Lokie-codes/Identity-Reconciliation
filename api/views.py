from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RequestSerializer, ResponseSerializer
from .models import Contact
from django.db.models import Q

@api_view(['POST'])
def reconcile_identity(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        email = data.get('email')
        phone_number = data.get('phoneNumber')

        if not email and not phone_number:
            return Response({"error": "At least one of 'email' or 'phoneNumber' must be provided."}, status=400)

        # Query contacts based on email OR phone number
        contacts = Contact.objects.all().order_by('createdAt')
        if email and phone_number:
            contacts = contacts.filter(Q(email=email) | Q(phoneNumber=phone_number))
        elif email:
            contacts = contacts.filter(email=email)
        elif phone_number:
            contacts = contacts.filter(phoneNumber=phone_number)

        if not contacts.exists():
            #  create a new contact if no matches found
            new_contact = Contact.objects.create(
                email=email,
                phoneNumber=phone_number,
                linkPrecedence=Contact.LinkPrecedence.PRIMARY
            )
            response_data = {
                "contact": {
                    "primaryContactId": new_contact.id,
                    "emails": [new_contact.email] if new_contact.email else [],
                    "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
                    "secondaryContactIds": []
                }
            }
            response_serializer = ResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=201)
            return Response(response_serializer.errors, status=400)

        # Find the earliest primary contact
        primary_contact = contacts.filter(linkPrecedence=Contact.LinkPrecedence.PRIMARY).order_by('createdAt').first()
        primary_contact_id = primary_contact.id if primary_contact else contacts.first().id

        # Gather all unique emails and phone numbers
        emails = list({c.email for c in contacts if c.email})
        phone_numbers = list({c.phoneNumber for c in contacts if c.phoneNumber})

        # Get all secondary contact IDs
        contacts = contacts.exclude(id=primary_contact_id)
        contacts.update(linkPrecedence=Contact.LinkPrecedence.SECONDARY, linkedId=primary_contact_id)
        secondary_contact_ids = list(contacts.values_list('id', flat=True))

        response_data = {
            "contact": {
                "primaryContactId": primary_contact_id,
                "emails": emails,
                "phoneNumbers": phone_numbers,
                "secondaryContactIds": secondary_contact_ids
            }
        }
        response_serializer = ResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=200)
        return Response(response_serializer.errors, status=400)
    return Response(serializer.errors, status=400)

