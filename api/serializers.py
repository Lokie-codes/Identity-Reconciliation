from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phoneNumber = serializers.CharField(max_length=15, required=False, allow_blank=True, allow_null=True)

    def validate(self, data):
        if not data.get('email') and not data.get('phoneNumber'):
            raise serializers.ValidationError("At least one of 'email' or 'phoneNumber' must be provided.")
        return data

class ContactSerializer(serializers.Serializer):
    primaryContactId = serializers.IntegerField(required=False, allow_null=True)
    emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False, allow_empty=True
    )
    phoneNumbers = serializers.ListField(
        child=serializers.CharField(max_length=15),
        required=False, allow_empty=True
    )
    secondaryContactIds = serializers.ListField(
        child=serializers.IntegerField(),
        required=False, allow_empty=True
    )

    def validate(self, data):
        if not data.get('primaryContactId') and not data.get('emails') and not data.get('phoneNumbers'):
            raise serializers.ValidationError("At least one of 'primaryContactId', 'emails', or 'phoneNumbers' must be provided.")
        return data
    
class ResponseSerializer(serializers.Serializer):
    contact = ContactSerializer()

    def validate_contact(self, value):
        if not value.get('primaryContactId') and not value.get('emails') and not value.get('phoneNumbers'):
            raise serializers.ValidationError("At least one of 'primaryContactId', 'emails', or 'phoneNumbers' must be provided in contact.")
        return value