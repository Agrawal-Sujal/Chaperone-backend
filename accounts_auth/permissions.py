from rest_framework import permissions

class IsWalker(permissions.BasePermission):
    
    # Allows access only to walker users.
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_walker is True)


class IsWanderer(permissions.BasePermission):

    # Allows access only to wanderer users.
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_walker is False)


class IsOwner(permissions.BasePermission):
    
    # User can only access their own data.
    def has_object_permission(self, request, view, obj):
        # Works with both User, Walker, or Wanderer objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
