from django.urls import reverse, resolve
from api.views import reconcile_identity

def test_identify_reconciliation_url_resolves():
    path = reverse('identify-reconciliation')
    assert path == '/identify/'
    resolver = resolve(path)
    assert resolver.func == reconcile_identity
    def test_identify_reconciliation_url_resolves():
        path = reverse('identify-reconciliation')
        assert path == '/identify/'
        resolver = resolve(path)
        assert resolver.func == reconcile_identity

    def test_identify_reconciliation_url_name():
        url = reverse('identify-reconciliation')
        assert url == '/identify/'

    def test_identify_reconciliation_url_resolves_to_correct_view():
        resolver = resolve('/identify/')
        assert resolver.func == reconcile_identity
