# myapp/permissions.py
from rest_framework import permissions


class IsOwnerOfObject(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    Assumes the object has a 'owner' or 'user' field.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user
