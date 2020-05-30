from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.utils import to_decimal

import requests
import requests as req


@shared_task
def parse_privatbank():
    from rate.models import Rate

    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.SOURCE_TYPE_USD,
        'EUR': mch.SOURCE_TYPE_EUR,
        'RUR': mch.SOURCE_TYPE_RUR,
    }
    for item in response.json():

        if item['ccy'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['ccy']]

        # buy
        amount = to_decimal(item['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(item['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_monobank():
    from rate.models import Rate

    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    currency_type_mapper = {
        840: mch.SOURCE_TYPE_USD,
        978: mch.SOURCE_TYPE_EUR,
        643: mch.SOURCE_TYPE_RUR,
    }

    for item in response.json():
        if item['currencyCodeA'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['currencyCodeA']]

        # buy
        amount = to_decimal(item['rateBuy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        amount = to_decimal(item['rateSell'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_vkurse():
    from rate.models import Rate
    url = "http://vkurse.dp.ua/course.json"
    response = requests.get(url).json()

    currency_type_mapper = {
        'Dollar': mch.SOURCE_TYPE_USD,
        'Euro': mch.SOURCE_TYPE_EUR,
        'Rub': mch.SOURCE_TYPE_RUR,
    }

    for item in response:
        if item not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item]

        # buy
        amount = to_decimal(response[item]['buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(response[item]['sale'])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_alfabnk():
    from rate.models import Rate

    resp = req.get("https://alfabank.ua/currency-exchange?refId=MainpageExchangerate")
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'currency-item-number'})
    rate_list = []
    for result in results:
        name = result.text
        rate_list.append(name)

    # USD_Buy
    amount = rate_list[0]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=1,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=1,
            type=2,
        )

    # USD_sale
    amount = rate_list[1]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=1,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=1,
            type=1,
        )

    # EUR_Buy
    amount = rate_list[2]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=2,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=2,
            type=2,
        )

    # EUR_sale
    amount = rate_list[1]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=2,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=2,
            type=1,
        )


@shared_task
def parse_otpbank():
    from rate.models import Rate

    resp = req.get("https://ru.otpbank.com.ua/")
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all('td', attrs={'class': 'currency-list__value'})
    rate_list = []
    for result in results:
        rate = result.text
        rate_list.append(rate)

    # USD_Buy
    amount = to_decimal(rate_list[0])
    last = Rate.objects.filter(
        source=mch.SOURCE_OTP,
        currency_type=1,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OTP,
            currency_type=1,
            type=2,
        )

    # USD_sale
    amount = to_decimal(rate_list[1])
    last = Rate.objects.filter(
        source=mch.SOURCE_OTP,
        currency_type=1,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OTP,
            currency_type=1,
            type=1,
        )

    # EUR_Buy
    amount = to_decimal(rate_list[3])
    last = Rate.objects.filter(
        source=mch.SOURCE_OTP,
        currency_type=2,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OTP,
            currency_type=2,
            type=2,
        )

    # EUR_sale
    amount = to_decimal(rate_list[4])
    last = Rate.objects.filter(
        source=mch.SOURCE_OTP,
        currency_type=2,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OTP,
            currency_type=2,
            type=1,
        )


@shared_task
def parse_ukrsibbank():
    from rate.models import Rate

    resp = req.get("https://my.ukrsibbank.com/ru/personal/")
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all('span', attrs={'class': 'rate__mob'})
    rate_list = []
    for result in results:
        rate = result.text
        rate_list.append(rate)

    # USD_Buy
    amount = rate_list[2]
    last = Rate.objects.filter(
        source=mch.SOURCE_UKRSIBBANK,
        currency_type=1,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_UKRSIBBANK,
            currency_type=1,
            type=2,
        )

    # USD_sale
    amount = rate_list[3]
    last = Rate.objects.filter(
        source=mch.SOURCE_UKRSIBBANK,
        currency_type=1,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_UKRSIBBANK,
            currency_type=1,
            type=1,
        )

    # EUR_Buy
    amount = rate_list[4]
    last = Rate.objects.filter(
        source=mch.SOURCE_UKRSIBBANK,
        currency_type=2,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_UKRSIBBANK,
            currency_type=2,
            type=2,
        )

    # EUR_sale
    amount = rate_list[5]
    last = Rate.objects.filter(
        source=mch.SOURCE_UKRSIBBANK,
        currency_type=2,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_UKRSIBBANK,
            currency_type=2,
            type=1,
        )


@shared_task
def parse():
    parse_monobank.delay()
    parse_privatbank.delay()
    parse_vkurse.delay()
    parse_alfabnk.delay()
    parse_otpbank.delay()
    parse_ukrsibbank.delay()
