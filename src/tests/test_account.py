from account.models import Contact

from django.core import mail
from django.urls import reverse


def test_sanity():
    assert 200 == 200


def test_contact_us_get_form(client):
    url = reverse('account:contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_empty_payload(client):
    assert len(mail.outbox) == 0
    initial_count = Contact.objects.count()
    url = reverse('account:contact-us')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 3
    assert errors['email_from'] == ['This field is required.']
    assert errors['message'] == ['This field is required.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_incorrect_payload(client):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail',
        'subject': 'hello world',
        'message': 'hello world\n' * 50,
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert errors['email_from'] == ['Enter a valid email address.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_login_get_form(client):
    url = reverse('account:login')
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name == ['registration/login.html']


def test_login_correct_data(admin_client):
    url = reverse('account:login')
    payload = {
        'username': 'admin',
        'password': 'password',
    }
    response = admin_client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_superuser is True
    assert response.wsgi_request.user.username == 'admin'
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.id == 1
    assert response.url == reverse('index')
