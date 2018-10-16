from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from .models import CaseType, Case
from .forms import PhaseForm
from .filters import CaseFilter

def startpage(request):
    return redirect('dashboard')

def dashboard(request):
    my_cases = Case.objects.filter(assignee=request.user)

    paginator = Paginator(my_cases, 50)

    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    index = page.number - 1
    page_range = paginator.page_range[max(0, index - 5):(min(len(paginator.page_range), index + 5))]

    return render(request, 'dashboard.html', {
        'page_range': page_range,
        'page': page
    })


def overview(request):
    cases = CaseFilter(request.GET, queryset=Case.objects.all())

    paginator = Paginator(cases.qs, 50)

    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    index = page.number - 1
    page_range = paginator.page_range[max(0, index - 5):(min(len(paginator.page_range), index + 5))]

    return render(request, 'overview.html', {
        'page_range': page_range,
        'page': page
    })


def create_case(request, case_type_id):
    case_type = get_object_or_404(CaseType, pk=case_type_id)
    phase = case_type.phases.first()

    if request.method == 'POST':
        form = PhaseForm(phase, request.POST)
        if form.is_valid():
            case = Case(name=_('Nieuwe zaak'), case_type=case_type, data=form.cleaned_data)
            case.save()

            messages.add_message(request, messages.INFO, _('Nieuwe zaak is aangemaakt.'))
            return redirect('view_case', case.id)
    else:
        form = PhaseForm(phase)

    return render(request, 'cases/create.html', {
        'case_type': case_type,
        'form': form
    })


def view_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    return render(request, 'cases/view.html', {
        'case': case
    })
