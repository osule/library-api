# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Book, Issue

User = get_user_model()

class UserTestCase(APITestCase): 
    def setUp(self):
        User.objects.create(
            email='test.admin@test.com', first_name='Test', 
            last_name='Admin', password='random', 
            username='test.admin', is_staff=True)
        super(UserTestCase, self).setUp()

    def test_can_get_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertIsInstance(data, list)


class BookTestCase(APITestCase): 
    def setUp(self):
        self.admin = User.objects.create(
            email='test.admin@test.com', first_name='Test', 
            last_name='Admin', password='random',
            username='test.admin', is_staff=True)
        super(BookTestCase, self).setUp()
    
    def test_can_get_books(self):
        response = self.client.get('/api/v1/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertIsInstance(data, list)
    
    def test_can_create_book(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/books/', data={
            'title': 'Book 1',
            'category': 'Arts',
            'isbn': '12344242',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.data
        self.assertEqual(data['title'], 'Book 1')

class IssuesTestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(**{
            'title': 'Book 1',
            'category': 'Arts',
            'isbn': '12344242',
        })
        self.user = User.objects.create(
            email='test.user@test.com', first_name='Test',
            last_name='User', password='random',
            username='test.user',
        )
        self.user2 = User.objects.create(
            email='test.user2@test.com', first_name='Test',
            last_name='User2', password='random',
            username='test.user2',
        )
        self.admin = User.objects.create(
            email='test.admin@test.com', first_name='Test', 
            last_name='Admin', password='random', 
            username='test.admin', is_staff=True
        )
        super(IssuesTestCase, self).setUp()
    
    def test_can_get_issues(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get('/api/v1/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertIsInstance(data, list)
    
    def test_can_request_unapproved_book(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/v1/issues/', {
            'book': self.book.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_cannot_request_approved_book(self):

        issue = Issue.objects.create(book=self.book, user=self.user, approved=True)

        self.client.force_authenticate(self.user2)

        response = self.client.get('/api/v1/books/')
        data = response.data
        for book in data:
            self.assertNotEqual(book['id'], self.book.id)

    def test_can_approve_issue(self):

        self.client.force_authenticate(self.admin)

        issue = Issue.objects.create(book=self.book, user=self.user)

        response = self.client.put('/api/v1/issues/{0.id}/'.format(issue), {
            'approved': True,
        })
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/issues/{0.id}/'.format(issue))
        data = response.data
        self.assertTrue(data['approved'])