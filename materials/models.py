from django.db import models

NULLABLE = {"blank": True, "null": True}


# Курс: Viewsets
# название,
# превью (картинка),
# описание.
# Урок: Generic-классы.
# название,
# описание,
# превью (картинка),
# ссылка на видео.


class Course(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/photo",
        verbose_name="Превью курса",
        help_text="Загрузите картинку для превью курса",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Укажите описание курса", **NULLABLE
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="lessons",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Укажите описание урока", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="lessons/photo",
        verbose_name="Превью урока",
        help_text="Загрузите картинку для превью урока",
        **NULLABLE
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео урока",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
