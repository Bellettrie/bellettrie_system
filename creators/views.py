from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
from creators.models import Creator


def get_authors_by_query(request, search_text):
    creators = Creator.objects.all()
    for word in search_text.split(" "):
        zz = Creator.objects.filter(Q(name__icontains=word) | Q(given_names__icontains=word))
        creators = creators & zz
    list = []
    for creator in creators:
        list.append({'id': creator.pk, 'text': creator.get_name()})
    return JsonResponse({'results': list}, safe=False)
