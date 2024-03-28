from django.apps import AppConfig


class MessagelocusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messagelocus'
    display_name = 'LOCUS Robotics'
    service = True
