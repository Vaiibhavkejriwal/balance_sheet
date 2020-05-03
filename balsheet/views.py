from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from balsheet.forms import BalSheetUploadForm
from core.services.file_upload import handle_uploaded_file
from balsheet.models import BalanceSheet
from core.constants import Constants


class Balsheet(View):
    def get(self, request):
        form = BalSheetUploadForm()
        return render(request, 'base.html', {"form": form})

    def post(self, request):
        form = BalSheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES["bal_sheet"]
            file_name = file_obj.name
            upload_dir = Constants.BAL_SHEET_INPUT_DIR.value
            try:
                handle_uploaded_file(upload_dir, file_name, file_obj)
            except Exception as e:
                print("There are some backend error please contact us")
                raise e

        balance_sheet = BalanceSheet(
            input_file_name=file_name,
            query_variable=request.POST["query_variable"],
            query_year=request.POST["query_year"]
            )
        balance_sheet.save()

        return render(request, 'base.html', {'form': form})
