python manage.py dumpdata materials > materials_data.json - создание фикстуры
python manage.py loaddata materials_data.json - команда загрузки сохраненных данных в текущую БД:

celery -A config worker -l INFO -P eventlet - команда для работы с celery
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler -  команда для работы django-celery-beat

celery -A my_project worker —loglevel=info
celery -A my_project beat —loglevel=info
__  Запуск Celery worker и планировщика Celery beat.
