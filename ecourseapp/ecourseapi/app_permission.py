from rest_framework import permissions

class CommentOwnerPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request=request, view=view) and request.user == obj.user