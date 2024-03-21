from rest_framework.permissions import BasePermission

class IsAdminOrIsSelf(BasePermission):
    """
    Custom permission to only allow admin users or the user themselves to access.
    """

    def has_permission(self, request, view):
        # Check if the user is an admin
        if request.user.is_superuser:
            return True
        
        # Check if the user is accessing their own detail
        user_id = view.kwargs.get('pk')
        if user_id and str(request.user.id) == user_id:
            return True
        
        return False
