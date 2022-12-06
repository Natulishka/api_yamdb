from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    '''
    Разрешение, что только автор может изменять и удалять контент
    '''
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.author


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


class IsSafeMethods(permissions.BasePermission):
    '''
    Разрешение безопасных методов
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsPostMethod(permissions.BasePermission):
    '''
    Разрешение метода post
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == 'POST':
                return True
        return False


class IsNotUser(permissions.BasePermission):
    '''
    Разрешение, что только модератор, администратор или суперюзер может
    изменять и удалять контент
    '''
    message = ('Только автор, модератор, администратор и суперюзер может '
               'изменять и удалять контент!')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role == 'admin':
                return True
            if request.user.role == 'moderator':
                return True
        return False
