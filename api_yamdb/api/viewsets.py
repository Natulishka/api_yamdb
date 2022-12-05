from rest_framework import mixins, viewsets


class CreateListDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает действия `retrieve` and 'update'.
    """
    pass


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает действия `create`.
    """
    pass
