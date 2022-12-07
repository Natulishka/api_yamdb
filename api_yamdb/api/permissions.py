from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    '''
    Разрешение, что только администратор и суперюзер может просматривать,
    изменять и удалять контент
    '''
    message = ('Только администратор и суперюзер может изменять и '
               'удалять контент!')

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin)


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    '''
    Разрешение, что только администратор и суперюзер может
    изменять и удалять контент, для остальных пользователей только чтение
    '''
    message = ('Только администратор и суперюзер может изменять и '
               'удалять контент!')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin)


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    '''
    Разрешение, что только модератор, администратор, суперюзер и автор может
    изменять и удалять контент, для остальных пользователей только чтение.
    Post запрос может делать только пользователь, прошедший аутентификацию.
    '''
    message = ('Только модератор, администратор, суперюзер и автор может'
               ' изменять и удалять контент! Post запрос может делать только'
               ' пользователь, прошедший аутентификацию!')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
            or request.user.is_moderator or request.user == obj.author)
