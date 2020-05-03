from balsheet.views import Balsheet
from django.urls import path

urlpatterns = [
    path('', Balsheet.as_view(), name='balsheet_upload')
]
