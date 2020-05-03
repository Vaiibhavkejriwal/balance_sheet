from django.db import models
from core.mixins import BaseModel


class BalanceSheet(BaseModel):
    input_file_name = models.CharField(null=True, blank=True, max_length=100)
    input_file_url = models.CharField(null=True, blank=True, max_length=100)
    output_file_name = models.CharField(null=True, blank=True, max_length=100)
    output_file_url = models.CharField(null=True, blank=True, max_length=100)
    query_variable = models.CharField(null=False, blank=False, max_length=50)
    query_year = models.IntegerField(null=False, blank=False, default=2020)

    def __str__(self):
        return "<BalanceSheet(input_file_name: {})>".format(self.input_file_name)
    