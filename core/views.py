from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.http import Http404
from django.contrib import messages
from .models import CaseType, Case, Phase
from .forms import PhaseForm, ChangeAssigneeForm, ChangePhaseForm
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
        'show_sidebar': True,
        'filter_form': cases.form,
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


def view_case(request, case_id, phase_id=None):
    case = get_object_or_404(Case, pk=case_id)

    if phase_id:
        try:
            phase = case.case_type.phases.get(pk=phase_id)
        except Phase.DoesNotExist:
            raise Http404('No Phase matches the given query.')
    else:
        phase = case.current_phase

    return render(request, 'cases/view.html', {
        'case': case,
        'selected_phase': phase,
        'form': PhaseForm(phase, initial=case.data) if phase else None
    })

def delete_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        case.delete()
        messages.add_message(request, messages.INFO, _('De zaak is verwijderd.'))
        return redirect('overview')

    return render(request, 'cases/delete.html', {
        'case': case,
    })

@require_http_methods(['POST'])
def claim(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if case.assignee:
        messages.add_message(request, messages.ERROR, _('Deze zaak is reeds in behandeling genomen.'))
        return redirect('view_case', case.id)

    case.assignee = request.user
    case.save()

    messages.add_message(request, messages.INFO, _('Je bent nu behandelaar van deze zaak.'))
    return redirect('view_case', case.id)

@require_http_methods(['POST'])
def next_phase(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    phases = list(case.case_type.phases.all())

    if not case.current_phase:
        new_phase = phases[1]
    else:
        old_index = phases.index(case.current_phase)

        try:
            new_phase = phases[old_index + 1]
        except IndexError:
            messages.add_message(request, messages.ERROR, _('Kan de zaak niet doorzetten naar de volgende fase.'))
            return redirect('view_case', case.id)

    case.current_phase = new_phase
    case.save()

    messages.add_message(request, messages.INFO, _('De zaak is doorgezet naar de volgende fase.'))
    return redirect('view_case', case.id)

def change_assignee(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        form = ChangeAssigneeForm(case, instance=case, data=request.POST)
        if form.is_valid():
            case.assignee = form.cleaned_data['assignee']
            case.save()

            messages.add_message(request, messages.INFO, _('De behandelaar is gewijzigd.'))
            return redirect('view_case', case.id)
    else:
        form = ChangeAssigneeForm(case, instance=case)

    return render(request, 'cases/change_assignee.html', {
        'case': case,
        'form': form
    })

def change_phase(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        form = ChangePhaseForm(case, instance=case, data=request.POST)
        if form.is_valid():
            case.current_phase = form.cleaned_data['current_phase']
            case.save()

            messages.add_message(request, messages.INFO, _('De fase is gewijzigd.'))
            return redirect('view_case', case.id)
    else:
        form = ChangePhaseForm(case, instance=case)

    return render(request, 'cases/change_phase.html', {
        'case': case,
        'form': form
    })

def attachments(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    return render(request, 'cases/attachments.html', {
        'case': case,
        'in_attachments': True
    })
