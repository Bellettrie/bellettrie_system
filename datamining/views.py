import datetime

from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from members.models import Member, Committee, MembershipPeriod, MembershipType, MemberBackground


def fetch_date(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return datetime.date(dt.year, dt.month, dt.day)


def find_members_by_request(request):
    members = Member.objects.all()
    found_members = []
    if request.GET.get('exec'):
        found_committees = request.GET.getlist('committees')
        found_privacy_things = request.GET.getlist('privacy')
        if request.GET.get('m_after'):
            for member in members:
                d = fetch_date(request.GET.get('m_after'))
                if member.end_date is not None and member.end_date > d:
                    found_members.append(member)
        else:
            found_members = list(members)

        if request.GET.get('m_before'):
            found_2 = []
            for member in found_members:
                d = fetch_date(request.GET['m_before'])
                if member.end_date is not None and member.end_date < d:
                    found_2.append(member)
            found_members = found_2
        if request.GET.get('m_include_honorary', False):
            for member in members:
                if member.end_date is None:
                    found_members.append(member)
        if len(found_committees) > 0:
            found_2 = []
            for member in found_members:
                found = False
                for committee in member.committees.all():
                    if str(committee.pk) in found_committees:
                        found = True
                if found:
                    found_2.append(member)
            found_members = found_2
        if len(found_privacy_things) > 0:
            found_2 = []
            for member in found_members:
                found = False
                if member.privacy_activities and 'activities' in found_privacy_things:
                    found = True
                if member.privacy_publications and 'publications' in found_privacy_things:
                    found = True
                if member.privacy_reunions and 'reunions' in found_privacy_things:
                    found = True
                if found:
                    found_2.append(member)
            found_members = found_2
    return found_members


@permission_required('members.view_member')
def show_members(request):
    committees = Committee.objects.all()
    found_members = find_members_by_request(request)
    r_str = ""

    for member in found_members:

        if len(member.email) > 0:
            r_str += ("; " + member.email)
    return render(request, 'data-mining-member-filtering.html', {'mails': request.GET.get('mails'), 'member_mail_addresses': r_str, 'members': found_members, 'committees': committees})


# Create your models here.


def get_member_statistics(day):
    members = MembershipPeriod.objects.filter((Q(start_date__lte=day) & Q(end_date__gte=day)) | Q(end_date__isnull=True))
    quadrants = dict()
    member_bg_counts = dict()
    member_type_counts = dict()
    r_mem = []
    for member in members:
        count = quadrants.get((member.member_background, member.membership_type), 0)
        quadrants[(member.member_background, member.membership_type)] = count + 1
        count = member_bg_counts.get(member.member_background, 0)
        member_bg_counts[member.member_background] = count + 1
        count = member_type_counts.get(member.membership_type, 0)
        member_type_counts[member.membership_type] = count + 1
        if member.membership_type is not None and member.member_background.name == 'employee':
            r_mem.append(member)
    zz = dict()

    for ru in MemberBackground.objects.all():
        zz[ru] = dict()
    zz[None] = dict()
    for ru in zz:
        for a in MembershipType.objects.all():
            zz[ru][a] = 0
        zz[ru][None] = 0
    for quad in quadrants.keys():
        row = zz.get(quad[0], dict())

        row[quad[1]] = quadrants[quad]
        zz[quad[0]] = row
    col_counts = dict()

    for row in zz.keys():
        if row is None:
            continue
        r_count = 0
        for z in zz[row].keys():
            if z is None:
                continue
            r_count += zz[row][z]
            col_counts[z] = col_counts.get(z, 0) + zz[row][z]
        zz[row]['Total'] = r_count
        col_counts['Total'] = col_counts.get('Total', 0) + r_count
    for row in zz.keys():
        zz[row].pop(None)
    zz.pop(None)
    zz['Total'] = col_counts
    return zz


@permission_required('members.view_member')
def show_membership_stats(request):
    dat = request.GET.get('date', datetime.datetime.now().date().isoformat())
    q = get_member_statistics(dat)
    return render(request, 'data-mining-member-stats.html', {'q': q})
