from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import IncomeSerializers
from .models import Income
from rest_framework import mixins, generics, status


class IncomelistApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = IncomeSerializers
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        if request.data['owner'] == str(request.user.id):
            return self.create(request, owner=self.request.user)
        else:
            return Response({"owner": "invalid user id"}, status=status.HTTP_400_BAD_REQUEST)


class IncomeDetailApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = IncomeSerializers
    queryset = Income.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

