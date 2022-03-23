import pytest

from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from lettings.models import Address, Letting


def test_url_lettings_index_page():
    """
    Teste si le nom de la vue est correct
    """
    path = reverse('lettings:lettings_index')
    view = resolve(path).func.__name__
    assert view == 'index'


@pytest.mark.django_db
def test_view_lettings_index_page():
    """
    Teste si une balise de titre est dans le template,
    et si le template retouné est lettings/index.html
    dans le dossier lettings
    """
    client = Client()
    path = reverse('lettings:lettings_index')
    address = Address.objects.create(number=1,
                                     street='rue de Paris',
                                     city='Bigcity',
                                     state='La comté',
                                     zip_code=10001,
                                     country_iso_code='LTM')
    Letting.objects.create(title='Hello world',
                           address=address)
    lettings_list = Letting.objects.all()
    response = client.get(path, {'lettings_list': lettings_list})
    content = response.content.decode()
    assert ("<title>" in content) and ("</title>" in content)
    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/index.html")


@pytest.mark.django_db
def test_template_lettings_index_page():
    """
    Teste si chacun des objets du modèle Letting
    apparait dans le template associé à lettings_index
    """
    client = Client()
    path = reverse('lettings:lettings_index')
    address1 = Address.objects.create(number=1,
                                      street='rue de Paris',
                                      city='Bigcity',
                                      state='La comté',
                                      zip_code=10001,
                                      country_iso_code='LTM')
    address2 = Address.objects.create(number=1,
                                      street='rue de Bruxelles',
                                      city='Bree',
                                      state='Frontier',
                                      zip_code=10101,
                                      country_iso_code='GDR')
    Letting.objects.create(title='Hello world',
                           address=address1)
    Letting.objects.create(title='What is new, doc ?',
                           address=address2)
    lettings_list = Letting.objects.all()
    response = client.get(path, {'lettings_list': lettings_list})
    content = response.content.decode()
    for letting in lettings_list:
        assert str(letting.title) in content


@pytest.mark.django_db
def test_url_lettings_detail_page():
    """
    Teste si le nom de la vue est correct,
    et si le chemin d'url contient l'id de l'objet
    """
    address = Address.objects.create(number=1,
                                     street='rue de Paris',
                                     city='Bigcity',
                                     state='La comté',
                                     zip_code=10001,
                                     country_iso_code='LTM')
    letting = Letting.objects.create(title='Hello world',
                                     address=address)
    letting_id = letting.id
    path = reverse('lettings:letting', kwargs={'letting_id': letting_id})
    partial_path = "/" + str(letting_id)
    view = resolve(path).func.__name__
    assert view == 'letting'
    assert partial_path in path


@pytest.mark.django_db
def test_view_lettings_detail_page():
    """
    Teste si une balise de titre est dans le template,
    et si le template retouné est lettings/index.html
    dans le dossier lettings
    """
    address = Address.objects.create(number=1,
                                     street='rue de Paris',
                                     city='Bigcity',
                                     state='La comté',
                                     zip_code=10001,
                                     country_iso_code='LTM')
    letting = Letting.objects.create(title='Hello world',
                                     address=address)
    letting_id = letting.id
    path = reverse('lettings:letting', kwargs={'letting_id': letting_id})
    client = Client()
    context = {
        'title': letting.title,
        'address': letting.address
    }
    response = client.get(path, context)
    content = response.content.decode()
    assert ("<title>" in content) and ("</title>" in content)
    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/letting.html")


@pytest.mark.django_db
def test_template_lettings_detail_page():
    """
    Teste si chacun des objets du modèle Letting
    apparait dans le template associé à lettings_index
    """
    address = Address.objects.create(number=1,
                                     street='rue de Paris',
                                     city='Bigcity',
                                     state='La comté',
                                     zip_code=10001,
                                     country_iso_code='LTM')
    letting = Letting.objects.create(title='Hello world',
                                     address=address)
    letting_id = letting.id
    path = reverse('lettings:letting', kwargs={'letting_id': letting_id})
    client = Client()
    context = {
        'title': letting.title,
        'address': letting.address
    }
    response = client.get(path, context)
    content = response.content.decode()
    assert str(letting.title) in content
    assert str(letting) in content
