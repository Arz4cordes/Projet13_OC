from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed


def test_url_home_page():
    """
    Teste si le nom de la vue est correct
    """
    path = reverse('index')
    view = resolve(path).func.__name__
    assert view == 'index'


def test_view_lettings_index_page():
    """
    Teste si une balise de titre est dans le template,
    et si le template retouné est index.html
    dans le dossier lettings
    """
    client = Client()
    path = reverse('index')
    response = client.get(path)
    content = response.content.decode()
    assert ("<title>" in content) and ("</title>" in content)
    assert response.status_code == 200
    assertTemplateUsed(response, "index.html")
