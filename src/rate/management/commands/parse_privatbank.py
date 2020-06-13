from datetime import datetime, timedelta
from mock import patch
from time import sleep
from django.utils import timezone

import requests
from django.core.management.base import BaseCommand

from rate.models import Rate
from rate import model_choices as mch


def date_range(start, end):
    # convert datetime to date
    if isinstance(start, datetime):
        start = start.date()

    # convert datetime to date
    if isinstance(end, datetime):
        end = end.date()

    for n in range((end - start).days):
        yield start + timedelta(n)


class Command(BaseCommand):
    help = 'Parse privatBank rates'  # noqa  help is python builtins but django command requires it.

    def handle(self, *args, **options):
        date_format = '%d.%m.%Y'
        start_date = datetime(2014, 12, 11)
        end_date = datetime.now()
        currency_type_mapper = {
            'USD': mch.SOURCE_TYPE_USD,
            'EUR': mch.SOURCE_TYPE_EUR,
            'RUB': mch.SOURCE_TYPE_RUR,
        }

        for date in date_range(start_date, end_date):
            sleep(10)
            url = f'https://api.privatbank.ua/p24api/exchange_rates' \
                  f'?json&date={date.strftime(date_format)}'
            response = requests.get(url)
            if response.status_code != 200:
                print(response.content)
                break

            rj = response.json()

            for rate in rj['exchangeRate']:
                currency = rate['currency']
                if currency not in currency_type_mapper:
                    continue

                currency_type = currency_type_mapper[currency]

                # sale
                amount = rate['saleRate']
                kwargs = {
                    'source': mch.SOURCE_PRIVATBANK,
                    'currency_type': currency_type,
                    'type': mch.RATE_TYPE_SALE,
                }
                if not Rate.objects.filter(created__date=date, **kwargs).exists():
                    with patch.object(timezone, 'now', return_value=date):
                        Rate.objects.create(
                            amount=amount,
                            **kwargs,
                        )

                # buy
                amount = rate['purchaseRate']
                kwargs = {
                    'source': mch.SOURCE_PRIVATBANK,
                    'currency_type': currency_type,
                    'type': mch.RATE_TYPE_BUY,
                }
                if not Rate.objects.filter(created__date=date, **kwargs).exists():
                    with patch.object(timezone, 'now', return_value=date):
                        Rate.objects.create(
                            amount=amount,
                            **kwargs,
                        )