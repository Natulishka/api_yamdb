from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    '''
    Разрешение, что только администратор и суперюзер может
    изменять и удалять контент
    '''
    message = ('Только администратор и суперюзер может изменять и '
               'удалять контент!')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role == 'admin':
                return True
        return False


class IsAdminOrSuperuserWithSafeMethods(permissions.BasePermission):
    '''
    Разрешение, что только администратор и суперюзер может
    изменять и удалять контент, для безопасных методов разрешение
    для любого пользователя
    '''
    message = ('Только администратор и суперюзер может изменять и '
               'удалять контент!')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role == 'admin':
                return True
        return False


class ReviewsAndCommentsPermissions(permissions.BasePermission):
    '''
    Разрешение, что только модератор, администратор, суперюзер и автор может
    изменять и удалять контент, для безопасных методов разрешение
    для любого пользователя. Post запрос может делать только
    пользователь, прошедший аутентификацию.
    '''
    message = ('Только модератор, администратор, суперюзер и автор может'
               ' изменять и удалять контент! Post запрос может делать только'
               ' пользователь, прошедший аутентификацию!')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role == 'admin':
                return True
            if request.user.role == 'moderator':
                return True
            if request.user == obj.author:
                return True
            return False
        return False
