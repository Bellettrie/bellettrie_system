import json

import markdown
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.forms import Widget
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template import loader
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from members.models import Member
from public_pages.django_markdown import DjangoUrlExtension
from public_pages.forms import PageEditForm, UploadFileForm
from public_pages.models import PublicPageGroup, PublicPage, FileUpload, ExternalUpload


def render_interrupt(markdown_text: str, title: str, *_):
    search_template = get_template('public_pages/elems/interrupt.html')
    return search_template.render(context={})


def render_md_section(markdown_text: str, title: str, medium: str, large: str, *_):
    md = markdown.Markdown(extensions=[DjangoUrlExtension(), 'tables', 'md_in_html', 'attr_list'])
    html = md.convert(markdown_text)
    search_template = get_template('public_pages/elems/basic_area.html')
    return search_template.render(context={"content": html, "sm": 12, "md": medium, "lg": large})


def render_square(markdown_text: str, title: str, medium: str, large: str, *_):
    md = markdown.Markdown(extensions=[DjangoUrlExtension(), 'tables', 'md_in_html', 'attr_list'])
    html = md.convert(markdown_text)
    search_template = get_template('public_pages/elems/square.html')
    return search_template.render(context={"content": html, "sm": 12, "md": medium, "lg": large, "title": title})


def render_find(markdown_text: str, title: str, medium: str, large: str, *_):
    md = markdown.Markdown(extensions=[DjangoUrlExtension(), 'tables', 'md_in_html', 'attr_list'])
    html = md.convert(markdown_text)
    search_template = get_template('public_pages/elems/search_field.html')
    return search_template.render(context={"content": html, "sm": 12, "md": medium, "lg": large})


def get_open():
    import urllib.request
    try:
        f = urllib.request.urlopen(settings.IS_OPEN_URL, timeout=120)
        is_open_result = str(f.read()).lower()
    except urllib.error.URLError:
        print("BROKEN")
        return False
    return "true" in is_open_result


def render_trafficlight(markdown_text: str, title: str, medium: str, large: str, *_):
    search_template = get_template('public_pages/elems/traffic_light.html')
    return search_template.render(context={"open": get_open(), "sm": 12, "md": medium, "lg": large})


CMDS = {
    "base": render_md_section,
    "square": render_square,
    "search": render_find,
    "light": render_trafficlight,
    "interrupt": render_interrupt,
}


def render_md(markdown_text: str):
    lines = ""
    result = ""
    title = ""
    cms = ["base", "-", "12", "12"]
    first_line = True
    for line in markdown_text.split("\n"):
        if line.startswith("#!title"):
            title = line[7:].strip()
        elif line.startswith("#!"):
            if not first_line:
                result += CMDS[cms[0]](lines, title, *cms[1:])
            cms = line[2:].strip().split(" ")
            lines = ""
        else:
            lines += "\n" + line
        first_line = False
    result += CMDS[cms[0]](lines, title, *cms[1:])
    return result


def forbid_showing_page(page: PublicPage, is_anonymous: bool, member: Member, current_date=None):
    committee_check = False
    if is_anonymous and (page.only_for_logged_in or page.only_for_current_members):
        return True
    if page.only_for_current_members and not member.is_currently_member(current_date):
        return True
    if len(page.limited_to_committees.all()) > 0:
        if is_anonymous:
            committee_check = True
        elif member is None:
            committee_check = True
        else:
            committee_check = True
            for c in page.limited_to_committees.all():
                if c in member.committees.all():
                    committee_check = False
    return committee_check


def view_named_page(request, page_name, sub_page_name):
    page_group = get_object_or_404(PublicPageGroup, name=page_name)

    can_edit = False

    if not request.user.is_anonymous and (request.user
                                          and (hasattr(request.user, 'member')
                                               and page_group.committees in request.user.member.committees.all())) \
            or request.user.has_perm('public_pages.change_publicpage'):
        can_edit = True

    page = get_object_or_404(PublicPage, name=sub_page_name, group=page_group)
    is_anonymous = request.user and request.user.is_anonymous
    member = hasattr(request.user, "member") and request.user.member
    if forbid_showing_page(page, is_anonymous, member):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    html = render_md(page.text)

    return HttpResponse(render(request, template_name='public_pages/public_page_simple.html',
                               context={'BASE_URL': settings.BASE_URL, 'markdown': page.text, 'page_title': page.title,
                                        'page_content': html, 'can_edit': can_edit, 'page': page}))


def view_page(page_name: str, sub_page_name: str):
    def view_function(request: HttpRequest):
        return view_named_page(request, page_name, sub_page_name)

    return view_function


@login_required
@csrf_exempt
def render_page_from_request(request):
    return HttpResponse(render_md(request.POST["text"]))


@login_required
def test_render_function(request):
    return HttpResponse(render(request, template_name='public_pages/page_edit.html', context={}))


@login_required
@transaction.atomic
def edit_named_page(request, page_name, sub_page_name):
    page_group = get_object_or_404(PublicPageGroup, name=page_name)
    page = get_object_or_404(PublicPage, name=sub_page_name, group=page_group)

    if forbid_showing_page(page, request.user.is_anonymous, request.user.member):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    can_edit = False
    if not request.user.is_anonymous and (
            request.user.member and page_group.committees in request.user.member.committees.all()) \
            or request.user.has_perm('public_pages.change_publicpage'):
        can_edit = True
    if not can_edit:
        return HttpResponse("cannot edit")

    if request.method == 'POST':
        form = PageEditForm(request.POST, instance=page)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('named_page', args=(page_name, sub_page_name)))
        else:
            print("ERROR")
    else:
        form = PageEditForm(instance=page)
    return render(request, 'public_pages/page_edit_form.html',
                  {'MY_URL': settings.BASE_URL, 'form': form, 'page': page})


@login_required()
@transaction.atomic
def new_named_page(request, page_name):
    page_group = get_object_or_404(PublicPageGroup, name=page_name)
    can_edit = False
    if not request.user.is_anonymous and (
            request.user.member and page_group.committees in request.user.member.committees.all()) \
            or request.user.has_perm('public_pages.change_publicpage'):
        can_edit = True
    if not can_edit:
        return HttpResponse("cannot edit")
    if request.method == 'POST':
        form = PageEditForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('named_page', args=(instance.group.name, instance.name)))
        else:
            print("ERROR")
    else:
        instance = PublicPage(group=page_group)
        form = PageEditForm(instance=instance)
    return render(request, 'public_pages/page_edit_form.html', {'MY_URL': settings.BASE_URL, 'form': form})


@permission_required('public_pages.view_publicpage')
def list_named_pages(request):
    pages = PublicPage.objects.all()
    return render(request, 'public_pages/page_list.html',
                  {'MY_URL': settings.BASE_URL, 'pages': pages, 'groups': PublicPageGroup.objects.all()})


@permission_required('public_pages.delete_publicpage')
@transaction.atomic
def delete_page(request, pk):
    page = PublicPage.objects.filter(pk=pk)
    if not request.GET.get('confirm'):
        return render(request, 'are-you-sure.html', {'what': "delete page with name " + page.first().name})

    page.delete()

    return redirect('list_pages')


def list_uploads(request):
    if not settings.EXTERNAL_UPLOAD_ENABLED:
        uploads = FileUpload.objects.all()
        return render(request, 'public_pages/uploads_list.html', {'uploads': uploads})
    else:
        uploads = ExternalUpload.objects.all()
        return render(request, 'public_pages/uploads_list.html', {'uploads': uploads})


@permission_required('public_pages.change_publicpage')
def new_upload(request):
    special = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            if not settings.EXTERNAL_UPLOAD_ENABLED:
                instance.save()
                special = "Succesful upload!"
            else:
                import requests
                url = settings.EXTERNAL_UPLOAD_URL_UPLOAD
                files = {}
                for file in request.FILES:
                    files[file] = request.FILES[file]
                r = requests.post(url + "?token=" + settings.EXTERNAL_UPLOAD_URL_API_KEY, files=files)
                tx = json.loads(r.text)
                for file in files:
                    nm = tx.get("Files").get(files[file].name)
                    if not nm:
                        print("File skipped")
                        continue
                    ExternalUpload.objects.create(external_name=nm, name=instance.name)
            form = UploadFileForm()
    else:
        form = UploadFileForm()

    return render(request, 'public_pages/upload_form.html', {"form": form, "special": special})


@permission_required('public_pages.change_publicpage')
def delete_upload(request, pk):
    if not settings.EXTERNAL_UPLOAD_ENABLED:
        page = FileUpload.objects.filter(pk=pk)
        if not request.GET.get('confirm'):
            return render(request, 'are-you-sure.html', {'what': "delete attachment with name " + page.first().name})
        page.delete()

        return redirect('list_uploads')
    else:
        page = ExternalUpload.objects.filter(pk=pk)
        if not request.GET.get('confirm'):
            return render(request, 'are-you-sure.html', {'what': "Delete attachment with name " + page.first().name})
        import requests
        url = settings.EXTERNAL_UPLOAD_URL_DELETE
        for file in page.all():
            print(url + "?token=" + settings.EXTERNAL_UPLOAD_URL_API_KEY + "&files=" + file.external_name)
            r = requests.post(url + "?token=" + settings.EXTERNAL_UPLOAD_URL_API_KEY + "&files=" + file.external_name)
            print(r.text)
            file.delete()

        return redirect('list_uploads')
