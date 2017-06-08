from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

from .serializers import UserSerializer, BookSerializer, IssueSerializer
from .models import Book, Issue, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be created, viewed, edited, deleted.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # TODO: filter out approved book
    @permission_classes((IsAdminUser,))
    def create(self, request):
        return super(BookViewSet, self).create(request)

    def list(self, request):
        serializer = BookSerializer(self.queryset.filter(approved=False), many=True)
        return Response(serializer.data)

class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be requested or approved.
    """

    queryset = Issue.objects.all().order_by('-created_at')
    serializer_class = IssueSerializer

    @permission_classes((IsAuthenticated,))
    def create(self, request):
        data = {
            'book': request.data.get('book'),
            'user': request.user.id,
        }
        serializer = IssueSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    @permission_classes((IsAdminUser,))
    def update(self, request, pk=None):
        issue = self.get_object()
        data = {
            'book': issue.book_id,
            'user': issue.user_id,
            'approved': request.data.get('approved'),
        }
        serializer = IssueSerializer(data=data)

        if serializer.is_valid():
            issue.approved = serializer.data['approved']
            issue.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

