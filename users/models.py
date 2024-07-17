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
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'наличные'),
        ('card', 'банковский перевод')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Платеж",
        related_name="Payment",
        **NULLABLE
    )
    date_payment = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        related_name="paid_course",
        **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        related_name="paid_lesson",
        **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты"
    )
    payment_method = models.CharField(
        max_length=35,
        choices=PAYMENT_METHOD_CHOICES,
        default='card',
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
