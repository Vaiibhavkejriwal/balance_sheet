from django import forms


class BalSheetUploadForm(forms.Form):
    bal_sheet = forms.FileField(
        label='Please Upload Balance Sheet',
        required=True,
        widget=forms.FileInput(attrs={'accept': 'application/pdf'}))
    query_variable = forms.CharField(
        label='Query Variable',
        max_length=50,
        required=True)
    query_year = forms.IntegerField(
        label='Query Year',
        required=True)
  
    def save(self):
        pass
