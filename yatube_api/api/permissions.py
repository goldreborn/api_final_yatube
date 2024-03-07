from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class OwnershipPermission(BasePermission):

    def has_object_permission(
            self, request: Request, view: object, obj: object
    ) -> bool:
        return (
            request.method in SAFE_METHODS or obj.author == request.user
        )
