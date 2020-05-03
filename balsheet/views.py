import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from balsheet.forms import BalSheetUploadForm
from core.services.file_upload import handle_uploaded_file
from core.services.file_download import download_file
from balsheet.models import BalanceSheet
from core.constants import Constants
from balsheet.services.bal_sheet_to_csv import PdfToCsvBalSheet
from balsheet.services.bal_sheet_service import BalSheetService


class Balsheet(View):
    def get(self, request):
        query_year = request.GET.get('queryYear')
        query_variable = request.GET.get('queryVariable')
        service = BalSheetService()
        uploaded_balsheets = service.get_balance_sheet(
            query_year, query_variable)   
        form = BalSheetUploadForm()
        return render(request,
                      'base.html',
                      {"form": form, "uploaded_balsheets": uploaded_balsheets})

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

        uploaded_balsheets = BalanceSheet.objects.order_by("-created_at").all()

        return render(request,
                      'base.html',
                      {'form': form, 'uploaded_balsheets': uploaded_balsheets})


class BalsheetDownloadCSV(View):
    def get(self, request, id):
        response = None
        file_obj = None
        try:
            file_obj = BalanceSheet.objects.get(pk=id)
        except Exception as e:
            print("Balance Sheet with {id} does not exist".format(id=id))
            raise e

        out_file_dir = Constants.BAL_SHEET_OUTPUT_DIR.value
        in_file_dir = Constants.BAL_SHEET_INPUT_DIR.value
        csv_file_name = file_obj.input_file_name.split(".")[0] + ".csv"
        csv_file_path = "{direct}/{file}".format(
            direct=out_file_dir,
            file=csv_file_name)

        if os.path.isfile(csv_file_path):
            response = download_file(csv_file_name, csv_file_path, "csv")
        else:
            pdf_to_csv = PdfToCsvBalSheet(
                file_obj.input_file_name,
                in_file_dir,
                out_file_dir)
            pdf_to_csv.pdf_to_csv_balsheet()
            file_obj.output_file_name = csv_file_name
            file_obj.save()
            response = download_file(csv_file_name, csv_file_path, "csv")

        return response
