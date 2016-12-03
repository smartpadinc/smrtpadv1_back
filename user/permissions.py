from rest_framework import permissions

class DefaultPermissions(permissions.BasePermission):

    def isAdmin(self):
        if self.request.user and self.request.user.is_staff:
            return True

    
