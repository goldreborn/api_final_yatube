from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class CreateListViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """Custom ViewSet"""
    pass
