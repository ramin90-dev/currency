SOURCE_PRIVATBANK = 1
SOURCE_MONOBANK = 2
SOURCE_VKURSE = 3
SOURCE_ALFABANK = 4
SOURCE_OTP = 5
SOURCE_UKRSIBBANK = 6

SOURCE_CHOICES = (
    (SOURCE_PRIVATBANK, 'PrivatBank'),
    (SOURCE_MONOBANK, 'MonoBank'),
    (SOURCE_VKURSE, 'Vkurse'),
    (SOURCE_ALFABANK, 'Alfabank'),
    (SOURCE_OTP, 'OTPBank'),
    (SOURCE_UKRSIBBANK, 'Ukrsibbank'),
)

SOURCE_TYPE_USD = 1
SOURCE_TYPE_EUR = 2
SOURCE_TYPE_RUR = 3

COURRENCY_TYPE_CHOICE = (
    (SOURCE_TYPE_USD, 'USD'),
    (SOURCE_TYPE_EUR, 'EUR'),
    (SOURCE_TYPE_RUR, 'RUR'),
)

RATE_TYPE_SALE = 1
RATE_TYPE_BUY = 2
RATE_TYPE_CHOICE = (
    (RATE_TYPE_SALE, 'Sale'),
    (RATE_TYPE_BUY, 'Buy'),
)
