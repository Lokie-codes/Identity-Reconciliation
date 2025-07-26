from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RequestSerializer, ResponseSerializer
from .models import Contact

@api_view(['POST'])
def reconcile_identity(request):
    pass