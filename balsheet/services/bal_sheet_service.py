from balsheet.models import BalanceSheet


class BalSheetService:
    def get_balance_sheet(self, query_year, query_variable):
        uploaded_balsheets = {}
        if query_year and query_variable:
                    uploaded_balsheets = BalanceSheet.objects.filter(
                        query_variable=query_variable,
                        query_year=query_year).order_by("-created_at").all()
        else:
            if query_year or query_variable:
                if query_year:
                    uploaded_balsheets = BalanceSheet.objects.filter(
                        query_year=query_year).order_by("-created_at").all()
                else:
                    uploaded_balsheets = BalanceSheet.objects.filter(
                        query_variable=query_variable).order_by("-created_at").all()
            else:
                uploaded_balsheets = BalanceSheet.objects.order_by("-created_at").all()

        return uploaded_balsheets
