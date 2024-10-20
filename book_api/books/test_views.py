import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book, Author, Genre

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_author():
    return Author.objects.create(name="Test Author", bio="Test Bio")

@pytest.fixture
def create_genre():
    return Genre.objects.create(name="Test Genre")

@pytest.fixture
def create_book(create_author):
    return Book.objects.create(title="Test Book", author=create_author, published_date="2024-10-19")

@pytest.mark.django_db
def test_create_book(api_client, create_author, create_genre):
    url = reverse('book-list')
    data = {
        "title": "New Book",
        "author": create_author.id,
        "genres": [create_genre.id],
        "published_date": "2024-10-19"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1
    assert Book.objects.get().title == "New Book"

@pytest.mark.django_db
def test_retrieve_book(api_client, create_book):
    url = reverse('book-detail', args=[create_book.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == create_book.title
    
@pytest.mark.django_db
def test_update_book(api_client, create_book, create_genre):
    url = reverse('book-detail', args=[create_book.id])
    data = {
        "title": "Updated Book",
        "author": create_book.author.id,
        "genres": [create_genre.id],  # Ensure at least one genre is included
        "published_date": "2024-10-19"
    }
    response = api_client.put(url, data, format='json')
    print(response.content)  # Add this line to print the response content
    assert response.status_code == status.HTTP_200_OK
    create_book.refresh_from_db()
    assert create_book.title == "Updated Book"
    
@pytest.mark.django_db
def test_delete_book(api_client, create_book):
    url = reverse('book-detail', args=[create_book.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0