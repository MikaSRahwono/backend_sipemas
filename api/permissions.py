from rest_framework.permissions import BasePermission
    
class IsManager(BasePermission):
    """
    Custom permission to only allow access to academic managers.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Manager').exists()
        return False

    
class IsSelf(BasePermission):
    """
    Custom permission to only allow the user themselves to access.
    """

    def has_permission(self, request, view):
        user_id = view.kwargs.get('pk')
        if user_id and str(request.user.id) == user_id:
            return True
        
        return False
    
class IsLecturer(BasePermission):
    """
    Custom permission to only allow access to lecturers.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Lecturer').exists()
        return False
    
class IsStudent(BasePermission):
    """
    Custom permission to only allow access to students.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Student').exists()
        return False
    
class IsSecretary(BasePermission):
    """
    Custom permission to only allow access to secretary.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Secretary').exists()
        return False
    
class IsInAllowedOrganizationsTopic(BasePermission):
    def has_object_permission(self, request, view, obj):
        course = obj.course
        user_groups = request.user.groups.all()
        return course.allowed_organizations.filter(id__in=user_groups).exists()