from django.urls import path
from .views import reconcile_identity

urlpatterns = [
    path('identify/', reconcile_identity, name='identify-reconciliation'),
]

