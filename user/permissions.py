from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCEO(BasePermission):
    """Only CEO can access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ceo')


class IsWaiter(BasePermission):
    """Only Waiter can access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'waiter')


class IsKitcher(BasePermission):
    """Only Kitchen staff can access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'kitcher')


class IsClient(BasePermission):
    """Only Client can access"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'client')


class IsCEOOrReadOnly(BasePermission):
    """Anyone authenticated can read, only CEO can write"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ceo')


class IsStaff(BasePermission):
    """Waiter, Kitcher or CEO can access"""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['waiter', 'kitcher', 'ceo']
        )


class IsStaffOrClient(BasePermission):
    """Any authenticated user can access — clients and staff"""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['client', 'waiter', 'kitcher', 'ceo']
        )


class CanManageOrders(BasePermission):
    """
    Clients can create orders (POST)
    Waiters and CEOs can do everything
    Kitchers can only read
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role = request.user.role

        if role == 'ceo' or role == 'waiter':
            return True
        if role == 'client' and request.method == 'POST':
            return True
        if role == 'kitcher' and request.method in SAFE_METHODS:
            return True

        return False