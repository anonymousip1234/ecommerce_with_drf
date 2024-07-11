from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,filters,permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import bulk_upload
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter



class BulkUploadView(APIView):
    def post(self, request):
        file_path = request.data['file_path']
        bulk_upload.delay(file_path)
        return Response({'status': 'Bulk upload started'})
    

class TaskListView(APIView):
    def get(self, request):
        i = inspect()
        scheduled_tasks = i.scheduled()
        return Response(scheduled_tasks)
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'price', 'stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['created_at']
    permission_classes = [permissions.IsAuthenticated]  # Require authentication
