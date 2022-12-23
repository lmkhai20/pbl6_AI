from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UploadSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from drf_yasg import openapi
from rest_framework.status import HTTP_400_BAD_REQUEST
import os


class UploadFile(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description='Upload Image...',
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='Image to be uploaded'),
        ]
    )
    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = UploadSerializer(data=request.data)


        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                HTTP_400_BAD_REQUEST
            )

        instance = serializer.save()



        print("Duong dan cua anh: ", instance.image)

        # Nhan dien
        # ...


        # Xoa anh sau khi nhan dien
        # os.remove(str(instance.image))

        return Response("sucess")

