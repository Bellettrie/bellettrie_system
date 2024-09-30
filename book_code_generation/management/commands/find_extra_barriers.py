from random import random, randint

import mysql.connector

from django.core.management.base import BaseCommand

from book_code_generation.models import CutterCodeResult, CutterCodeRange
from book_code_generation.helpers import normalize_str, normalize_number
from creators.models import CreatorLocationNumber, LocationNumber


# noinspection DuplicatedCode
def get_key(obj):
    return obj.name


class Command(BaseCommand):
    help = 'Displays out-of-order authors'

    def handle(self, *args, **options):
        from works.models import Location
        for location in Location.objects.all():
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                codes = CutterCodeRange.objects.all()
                lst = []
                for code in codes:
                    if code.from_affix.startswith(letter):
                        lst.append(CutterCodeResult(normalize_str(code.from_affix), normalize_number(code.number)))

                letters = list(LocationNumber.objects.filter(location=location, letter=letter))
                for item in letters:
                    lst.append(CutterCodeResult(normalize_str(item.name), item.number))
                lst.sort(key=get_key)
                prev = None
                num = 0
                for item in lst:
                    if str(num) > str(item.number):
                        if prev:
                            print(item.name, item.number, num, prev, location)
                        else:
                            print(item.name, item.number, num, location)
                    num = item.number
                    prev = item.name
