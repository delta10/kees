from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
import reversion
from .models import Case, Attachment
from .serializers import CaseSerializer, AttachmentSerializer


class CaseViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    http_method_names = ['head', 'get', 'post', 'patch']

    def perform_create(self, serializer):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_closed:
           raise PermissionDenied('Kan de velden niet opslaan omdat de zaak gesloten is.')

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_update(serializer)

    def perform_destroy(self, instance):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_destroy(instance)


class AttachmentViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    http_method_names = ['head', 'get', 'post', 'patch']

    def perform_create(self, serializer):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.case.is_closed:
           raise PermissionDenied('Kan de velden niet opslaan omdat de zaak gesloten is.')

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_update(serializer)

    def perform_destroy(self, instance):
        with reversion.create_revision():
            reversion.set_user(self.request.user)
            return super().perform_destroy(instance)
