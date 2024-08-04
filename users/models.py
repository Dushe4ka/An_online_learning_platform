from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Укажите телефон", **NULLABLE
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", help_text="Укажите город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Укажите аватар",
        **NULLABLE
    )
    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name='Заходил в последний раз',
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# Платежи
#
# пользователь,
# дата оплаты,
# оплаченный курс или урок,
# сумма оплаты,
# способ оплаты: наличные или перевод на счет.
class Payment(models.Model):
    from materials.models import Course, Lesson

    class Type_payment(models.TextChoices):
        cash = 'Наличные'
        transfer = 'Переводом'

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', related_name='payment',
                              **NULLABLE)
    datetime_payment = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True, **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='сумма оплаты', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    payment_type = models.CharField(choices=Type_payment.choices, max_length=16, verbose_name='способ оплаты', default='Наличные')
    session_id = models.CharField(max_length=300, verbose_name=' id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'Оплата {self.owner.email} на {self.price} руб.'
