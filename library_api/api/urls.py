from rest_framework import routers
from .viewsets import UserViewSet, BookViewSet, IssueViewSet

router = routers.DefaultRouter()


router.register('users', UserViewSet)
router.register('books', BookViewSet)
router.register('issues', IssueViewSet)