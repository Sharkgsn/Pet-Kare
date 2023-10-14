from rest_framework.views import Request, Response, APIView, status
from .models import Group
from .serializers import GroupSerializer


class GroupView(APIView):
    def post(self, req: Request) -> Response:
        serializer = GroupSerializer(data=req.data)
