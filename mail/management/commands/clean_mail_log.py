from django.core.management.base import BaseCommand

from lendings.procedures.mail_late import late_mails
from mail.models import MailLog


class Command(BaseCommand):
    help = 'clean mail log'

    def handle(self, *args, **options):
        for mail in MailLog.objects.filter(sent=True, date__lte=get_today() - timedelta(days=60)):
            mail.delete()
