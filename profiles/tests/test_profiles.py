import pytest

from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from profiles.models import Profile
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_url_lettings_index_page():
    """
    Teste si le nom de la vue est correct
    """
    path = reverse('profiles:profiles_index')
    view = resolve(path).func.__name__
    assert view == 'profiles_index'


@pytest.mark.django_db
def test_view_profiles_index_page():
    """
    Teste si une balise de titre est dans le template,
    et si le template retouné est lettings/index.html
    dans le dossier lettings
    """
    client = Client()
    path = reverse('profiles:profiles_index')
    first_user = User.objects.create(username='Beatrice',
                                     email='bea13@mail.com',
                                     password='mysecretpassword1')
    second_user = User.objects.create(username='Charles',
                                      email='charles@mail.com',
                                      password='mysecretpassword2')
    Profile.objects.create(user=first_user,
                           favorite_city='Rennes')
    Profile.objects.create(user=second_user,
                           favorite_city='Brest')
    profiles_list = Profile.objects.all()
    response = client.get(path, {'profiles_list': profiles_list})
    content = response.content.decode()
    assert ("<title>" in content) and ("</title>" in content)
    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profiles_index.html")


@pytest.mark.django_db
def test_template_profiles_index_page():
    """
    Teste si chacun des objets du modèle Letting
    apparait dans le template associé à lettings_index
    """
    client = Client()
    path = reverse('profiles:profiles_index')
    first_user = User.objects.create(username='Beatrice',
                                     email='bea13@mail.com',
                                     password='mysecretpassword1')
    second_user = User.objects.create(username='Charles',
                                      email='charles@mail.com',
                                      password='mysecretpassword2')
    Profile.objects.create(user=first_user,
                           favorite_city='Rennes')
    Profile.objects.create(user=second_user,
                           favorite_city='Brest')
    profiles_list = Profile.objects.all()
    response = client.get(path, {'profiles_list': profiles_list})
    content = response.content.decode()
    for profile in profiles_list:
        assert str(profile.user.username) in content


@pytest.mark.django_db
def test_url_profiles_detail_page():
    """
    Teste si le nom de la vue est correct,
    et si le chemin d'url contient l'id de l'objet
    """
    first_user = User.objects.create(username='Beatrice',
                                     email='bea13@mail.com',
                                     password='mysecretpassword1')
    the_name = first_user.username
    Profile.objects.create(user=first_user,
                           favorite_city='Rennes')
    path = reverse('profiles:profile', kwargs={'username': the_name})
    partial_path = "/" + str(the_name)
    view = resolve(path).func.__name__
    assert view == 'profile'
    assert partial_path in path


@pytest.mark.django_db
def test_view_profiles_detail_page():
    """
    Teste si une balise de titre est dans le template,
    et si le template retouné est lettings/index.html
    dans le dossier lettings
    """
    first_user = User.objects.create(username='Beatrice',
                                     email='bea13@mail.com',
                                     password='mysecretpassword1')
    the_name = first_user.username
    profile = Profile.objects.create(user=first_user,
                                     favorite_city='Rennes')
    path = reverse('profiles:profile', kwargs={'username': the_name})
    client = Client()
    context = {'profile': profile}
    response = client.get(path, context)
    content = response.content.decode()
    assert ("<title>" in content) and ("</title>" in content)
    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile.html")


@pytest.mark.django_db
def test_template_profiles_detail_page():
    """
    Teste si chacun des objets du modèle Letting
    apparait dans le template associé à lettings_index
    """
    first_user = User.objects.create(username='Beatrice',
                                     email='bea13@mail.com',
                                     password='mysecretpassword1')
    the_name = first_user.username
    profile = Profile.objects.create(user=first_user,
                                     favorite_city='Rennes')
    path = reverse('profiles:profile', kwargs={'username': the_name})
    client = Client()
    context = {'profile': profile}
    response = client.get(path, context)
    content = response.content.decode()
    assert str(profile) in content
    assert str(profile.user.email) in content
