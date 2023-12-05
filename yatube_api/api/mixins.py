from rest_framework import mixins, viewsets


class CreateListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Кастомный вьюсет для чтения списка или создания объекта.
    """

    pass
