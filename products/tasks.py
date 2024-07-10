from celery import shared_task
from .models import Product
import csv

@shared_task
def bulk_upload(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Product.objects.create(**row)