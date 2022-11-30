from rest_framework import mixins, viewsets


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает действия `create`.
    """
    pass
