from balsheet.views import Balsheet, BalsheetDownloadCSV
from django.urls import path

urlpatterns = [
    path('balsheet', Balsheet.as_view(), name='balsheet_upload'),
    path('downloadcsv/<int:id>/', BalsheetDownloadCSV.as_view(), name='download_balsheet_csv')
]
