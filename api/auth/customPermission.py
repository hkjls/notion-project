from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return
    
    def has_object_permission(self, request, view, obj):
        return