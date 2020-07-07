from random import random, randint

import mysql.connector

from django.core.management.base import BaseCommand

from bellettrie_library_system.settings import OLD_DB, OLD_USN, OLD_PWD
from book_code_generation.models import CutterCodeRange
from members.management.commands.namegen import generate_name, generate_full_name
from members.models import Member
from works.models import Item, Creator


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        cutter = CutterCodeRange.get_cutter_number("Pratchett")
        print(cutter.generated_affix)
