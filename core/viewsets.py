from rest_framework import viewsets
import reversion
from .models import Case
from .serializers import CaseSerializer


class CaseViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    http_method_names = ['head', 'get', 'post', 'patch']

    def perform_create(self, serializer):
        with reversion.create_revision():
            super().perform_create(serializer)
            reversion.set_user(self.request.user)

    def perform_update(self, serializer):
        with reversion.create_revision():
            super().perform_update(serializer)
            reversion.set_user(self.request.user)

    def perform_destroy(self, instance):
        with reversion.create_revision():
            super().perform_destroy(instance)
            reversion.set_user(self.request.user)
