from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_information_about_enrolling(course_title, student_name, student_email, teacher_email):
    """ Отправляет информацию о зачислении студента на курс. """

    send_mail(
        "Информация о зачислении",
        f"На Ваш курс {course_title} зачислен студент {student_name} - {student_email}.",
        settings.EMAIL_HOST_USER,
        [teacher_email],
        fail_silently=False)
