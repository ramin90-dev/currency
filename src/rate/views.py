import csv

from datetime import datetime
from openpyxl import Workbook

from django.http import HttpResponse
from django.views.generic import ListView, View, TemplateView


from rate.models import Rate
from rate.utils import display


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'list_all.html'


class RateDownloadCSV(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'amount',
        'type',
    )
    queryset = Rate.objects.all().iterator()

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = self.get_response()

        writer = csv.writer(response)
        writer.writerow(self.__class__.HEADERS)

        for rate in self.queryset:
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))

            writer.writerow(values)

        return response


    def get_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rate.csv"'
        return response




class RateDownloadXLSX(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'amount',
        'type',
    )
    queryset = Rate.objects.all().iterator()
    def get(self, request):

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        today = datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename={today}-rates_all.xlsx'
        workbook = Workbook()

        # Get active worksheet/tab
        worksheet = workbook.active
        worksheet.title = 'Rates_all'

        # Define the titles for columns
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(self.HEADERS, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Iterate through all movies
        for rate in self.queryset:
            row_num += 1
            # row
            row = []
            for attr in self.__class__.HEADERS:
                row.append(display(rate, attr))

            # Assign the data for each cell of the row
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        workbook.save(response)

        return response

class LatestRatesView(TemplateView):
    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object_list = []

        for source in mch.SOURCE_CHOICES:  # source
            source = source[0]
            for currency in mch.CURRENCY_TYPE_CHOICES:  # currency_type
                currency = currency[0]
                for rate_type in mch.RATE_TYPE_CHOICES:  # rate_type
                    rate_type = rate_type[0]
                    rate = Rate.objects.filter(source=source,
                                               currency_type=currency,
                                               rate_type=rate_type).last('created')
                    if rate is not None:
                        object_list.append(rate)

        context['object_list'] = object_list
        return context
