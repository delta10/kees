from rest_framework import viewsets
from .models import Case
from .serializers import CaseSerializer


class CaseViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    http_method_names = ['head', 'get', 'post', 'patch']
