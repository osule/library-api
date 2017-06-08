from rest_framework import viewsets

from .serializers import UserSerializer, BookSerializer, IssueSerializer
from .models import Book, Issue, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_created')
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be created, viewed, edited, deleted.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # TODO: filter out approved book
    # TODO: can only create books if admin

class IssueSerializer(viewsets.IssueSerializer):
    """
    API endpoint that allows issues to be requested or approved.
    """
    queryset = Issue.objects.all().order_by('-created_at')
    serializer_class = IssueSerializer
