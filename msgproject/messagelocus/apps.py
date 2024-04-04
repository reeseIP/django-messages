from django.apps import AppConfig


class MessagelocusConfig(AppConfig):
    
    name = 'messagelocus'
    default_auto_field = 'django.db.models.BigAutoField'
    display_name = 'LOCUS Robotics'
    service = True
