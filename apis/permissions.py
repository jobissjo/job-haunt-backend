from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrAuthenticatedReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users (is_staff=True) have full access.
    - Authenticated users can read-only.
    - Others are denied.
    """

    def has_permission(self, request, view):
        # ✅ Allow full access to admin/staff
        if request.user and request.user.is_staff:
            return True
        
        # ✅ Allow read-only access (GET, HEAD, OPTIONS) to authenticated users
        if request.user and request.user.is_authenticated and request.method in SAFE_METHODS:
            return True

        # 🚫 Deny all others
        return False
