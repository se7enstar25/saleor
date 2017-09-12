from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import GroupForm
from ..views import staff_member_required
from ...core.utils import get_paginator_items
from ...userprofile.models import User


@staff_member_required
def staff_list(request):
    staff_members = (
        User.objects
        .filter(is_staff=True)
    )
    staff_members = get_paginator_items(
        staff_members, 30, request.GET.get('page'))
    ctx = {'staff': staff_members}
    return TemplateResponse(request, 'dashboard/staff/list.html', ctx)


@staff_member_required
def staff_details(request, pk):
    queryset = User.objects.filter(is_staff=True)
    staff_member = get_object_or_404(queryset, pk=pk)

    form = GroupForm(request.POST or None, instance=staff_member)
    if form.is_valid():
        form.save()

    ctx = {'staff_member': staff_member,
           'form': form}
    return TemplateResponse(request, 'dashboard/staff/detail.html', ctx)
