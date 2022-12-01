from rest_framework import mixins, viewsets


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает действия `retrieve` and 'update'.
    """
    pass
