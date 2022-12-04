from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''
    Разрешение, что только автор может изменять и удалять контент
    '''
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsAdminOrSuperuser(permissions.BasePermission):
    '''
    Разрешение, что только администратор и суперюзер может изменять и
    удалять контент
    '''
    message = ('Только администратор и суперюзер может изменять и '
               'удалять контент!')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.role == 'admin':
            return True
        return False


class IsModerator(permissions.BasePermission):
    '''
    Разрешение, что только модератор может изменять и
    удалять контент
    '''
    message = ('Только модератор может изменять и'
               'удалять контент!')

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False


class IsSafeMethods(permissions.BasePermission):
    '''
    Разрешение безопасных методов
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
