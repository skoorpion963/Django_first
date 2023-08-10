# import os
# from celery import Celery
# # from polls.density_search import main as density_search
# # from polls.upload_volume_1 import main as upload_volume



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')

# app = Celery('firstproject')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# # app.task(density_search,bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})

# # app.task(upload_volume)

# app.conf.beat_schedule = {
#     'my-periodic-task1': {
#         'task': 'polls.tasks.tableV1_update',
#         'schedule': 3.0,  # 2сек кд
#     },
#      'my-periodic-task2': {
#         'task': 'polls.tasks.table_update',
#         'schedule': 5.0, 
#     },
# }


import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')

app = Celery('firstproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




app.conf.beat_schedule = {
    'my-periodic-task1': {
        'task': 'polls.tasks.tableV1_update',
        'schedule': 3.0,  # 2сек кд
    },
     'my-periodic-task2': {
        'task': 'polls.tasks.table_update',
        'schedule': 5.0, 
    },
}
