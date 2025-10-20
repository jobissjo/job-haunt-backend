from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.models import CustomUser, JobSkills
from rest_framework import status
from django.apps import apps
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAdminUser
from django.core import serializers
import json
from apis.serializers import FileSerializer
from django.conf import settings

class AdminStatsView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        stats = {
            "totalUsers": CustomUser.objects.filter(role="user").count(),
            "totalSkills": JobSkills.objects.count(),
            "recentActivity": 0,
        }
        return Response(stats, status=status.HTTP_200_OK)


class ExportAllTablesView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        all_data = {}

        for model in apps.get_models():
            queryset = model.objects.all()
            json_data = serializers.serialize('json', queryset)
            all_data[model._meta.label] = json.loads(json_data)

        response = HttpResponse(
            json.dumps(all_data, indent=4),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="database_export.json"'
        return response



class ImportJSONView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        json_file = request.FILES.get("file")
        secret_token = request.data.get('secret_token')

        if secret_token != settings.SECRET_OPERATION_TOKEN:
            if not (request.user.is_authenticated and request.user.is_superuser):
                return Response({"error": "Invalid secret token."}, status=status.HTTP_401_UNAUTHORIZED)

        if not json_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            all_data = json.load(json_file)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON file."}, status=status.HTTP_400_BAD_REQUEST)

        for model_label, data_json in all_data.items():
            app_label, model_name = model_label.split('.')
            try:
                model = apps.get_model(app_label=app_label, model_name=model_name)
            except LookupError:
                continue  # skip unknown models

            # Serialize each object in the list
            json_data_str = json.dumps(data_json)
            for obj in serializers.deserialize('json', json_data_str):
                obj.save()  # save to DB

        return Response({"message": "Data imported successfully!"}, status=status.HTTP_201_CREATED)