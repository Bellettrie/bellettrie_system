from django.urls import path

from members.permissions import MEMBERS_LIST, MEMBERS_NEW, MEMBERS_VIEW, MEMBERS_EDIT
from members.views import MemberList, signup, delete_user, change_user, remove_user
from . import views
from .views import get_authors_by_query

urlpatterns = [

    path('search/<search_text>', get_authors_by_query, name='authors.query'),

]
