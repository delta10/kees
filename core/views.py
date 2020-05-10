from django.db.models import F
from django.db.models.expressions import RawSQL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.middleware import csrf
from django.template import Template, Context
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.http import Http404
from django.contrib import messages
from constance import config
import reversion
from .models import CaseType, Case, Phase, Field, Attachment
from .forms import ChangeAssigneeForm, ChangePhaseForm, AttachmentForm
from .filters import CaseFilter

def startpage(request):
    return redirect('dashboard')

def dashboard(request):
    groups = request.user.groups.all()
    phases = Phase.objects.filter(assign_to__in=groups)

    intake = Case.objects.filter(current_phase__in=phases, assignee=None)
    intake_paginator = Paginator(intake, 10)

    try:
        intake_page = intake_paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        intake_page = intake_paginator.page(1)
    except EmptyPage:
        intake_page = intake_paginator.page(intake_paginator.num_pages)

    index = intake_page.number - 1
    intake_page_range = intake_paginator.page_range[max(0, index - 5):(min(len(intake_paginator.page_range), index + 5))]

    return render(request, 'dashboard.html', {
        'intake_paginator': intake_paginator,
        'intake_page_range': intake_page_range,
        'intake_page': intake_page,
        'my_cases': Case.objects.filter(assignee=request.user)
    })


def case_list(request):
    queryset = Case.objects.all()

    if not request.GET.get('status'):
        queryset = queryset.filter(current_phase__isnull=False)

    order_by = request.GET.get('order_by', 'id')

    if request.GET.get('direction') == 'asc':
        direction = 'asc'
    else:
        direction = 'desc'

    if order_by in ['id', 'name', 'case_type', 'created_at', 'current_phase']:
        if direction == 'desc':
            queryset = queryset.order_by(F(order_by).desc(nulls_last=True))
        else:
            queryset = queryset.order_by(F(order_by).asc(nulls_last=True))
    else:
        if direction == 'desc':
            queryset = queryset.order_by(RawSQL("data->>%s", (order_by, )).desc(nulls_last=True))
        else:
            queryset = queryset.order_by(RawSQL("data->>%s", (order_by, )).asc(nulls_last=True))


    additional_filters = _get_additional_fields(config.ADDITIONAL_FILTERS)
    additional_fields = _get_additional_fields(config.ADDITIONAL_FIELDS)

    for additional_filter in additional_filters:
        if request.GET.get(additional_filter.key):
            queryset = queryset.filter(data__contains={additional_filter.key: request.GET.get(additional_filter.key)})

    case_filter = CaseFilter(request.GET, queryset=queryset, request=request)
    paginator = Paginator(case_filter.qs, 50)

    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    index = page.number - 1
    page_range = paginator.page_range[max(0, index - 5):(min(len(paginator.page_range), index + 5))]

    return render(request, 'cases.html', {
        'show_sidebar': True,
        'order_by': order_by,
        'direction': direction,
        'filter_form': case_filter.form,
        'additional_filters': additional_filters,
        'additional_fields': additional_fields,
        'paginator': paginator,
        'page_range': page_range,
        'page': page
    })

def _get_additional_fields(field_keys):
    if not field_keys:
        return []

    field_keys = field_keys.split(',')

    fields = []
    for field_key in field_keys:
        try:
            fields.append(Field.objects.get(key=field_key))
        except Field.DoesNotExist:
            pass

    return fields

def create_case(request, case_type_id):
    if not config.CREATE_CASE:
        messages.add_message(request, messages.ERROR, _('Het creëren van zaken is uitgeschakeld.'))
        return redirect('dashboard')

    case_type = get_object_or_404(CaseType, pk=case_type_id)
    phase = case_type.phases.first()

    return render(request, 'cases/create.html', {
        'case_type': case_type,
        'js_phase_form_data': {
            'formItems': _get_form_items(phase),
            'disabled': False,
            'case': {
                'id': None,
                'data': {},
                'initialData': {}
            },
            'caseType': {
                'id': case_type.id
            },
            'csrftoken': csrf.get_token(request)
        }
    })


def view_case(request, case_id, phase_id=None):
    case = get_object_or_404(Case, pk=case_id)

    if phase_id:
        try:
            phase = case.case_type.phases.get(pk=phase_id)
        except Phase.DoesNotExist:
            raise Http404('No Phase matches the given query.')
    elif case.is_open:
        phase = case.current_phase
    else:
        phase = case.case_type.phases.last()

    return render(request, 'cases/view.html', {
        'case': case,
        'selected_phase': phase,
        'templates': _render_templates(phase, case),
        'js_phase_form_data': {
            'formItems': _get_form_items(phase),
            'disabled': case.is_closed,
            'case': {
                'id': case.id,
                'data': case.data,
                'initialData': case.data
            },
            'csrftoken': csrf.get_token(request)
        }
    })

def _get_form_items(phase):
    fields = []

    for item in phase.fields:
        field = _get_field(item)

        if field['type'] == 'Template':
            continue

        fields.append({'field': field})

    return fields

def _get_field(key):
    field = Field.objects.get(key=key).toDict()

    if field['type'] == 'ArrayField':
        field['args']['formItems'] = [{'field': _get_field(key)} for key in field['args'].get('formItems', [])]

    return field

def _render_templates(phase, case):
    templates = []

    for item in phase.fields:
        field = Field.objects.get(key=item).toDict()

        if field['type'] == 'Template':
            template = Template(field['args'].get('template'))
            context = Context({'case': case})
            templates.append(template.render(context))

    return templates

@permission_required('core.can_manage_cases', raise_exception=True)
def delete_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        with reversion.create_revision():
            case.delete()
            reversion.set_user(request.user)

        messages.add_message(request, messages.INFO, _('De zaak is verwijderd.'))
        return redirect('cases')

    return render(request, 'cases/delete.html', {
        'case': case,
    })

@require_http_methods(['POST'])
def claim_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if case.assignee:
        messages.add_message(request, messages.ERROR, _('Deze zaak is reeds in behandeling genomen.'))
        return redirect('view_case', case.id)

    case.assignee = request.user
    case.save()

    case.logs.create(event='claim_case', performer=request.user.to_dict())

    messages.add_message(request, messages.INFO, _('Je bent nu behandelaar van deze zaak.'))
    return redirect('view_case', case.id)

@require_http_methods(['POST'])
def next_phase(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    missing_fields = []
    if case.current_phase:
        for item in case.current_phase.fields:
            field = Field.objects.get(key=item)

            if field.type == 'Heading' or field.type == 'Template':
                continue

            required = field.args.get('required')
            if isinstance(required, bool) and not required:
                continue

            if not case.data.get(field.key):
                missing_fields.append(field.label)

    if len(missing_fields) > 0:
        messages.add_message(
            request,
            messages.ERROR,
            _('Kan de zaak niet doorzetten naar de volgende fase omdat de volgende velden ontbreken: {}.'.format(', '.join(missing_fields)))
        )

        return redirect('view_case', case.id)

    try:
        old_phase = str(case.current_phase) if case.current_phase else None

        if case.current_phase == case.last_phase:
            case.close()
            messages.add_message(request, messages.INFO, _('De zaak is afgesloten.'))

            case.logs.create(event='closed_case', performer=request.user.to_dict(), metadata={
                'old_phase': old_phase,
            })

            return redirect('cases')

        case.next_phase(request)
        messages.add_message(request, messages.INFO, _('De zaak is doorgezet naar de volgende fase.'))

        case.logs.create(event='next_phase', performer=request.user.to_dict(), metadata={
            'old_phase': old_phase,
            'new_phase': str(case.current_phase) if case.current_phase else None,
        })

        return redirect('view_case', case.id)

    except IndexError:
        messages.add_message(request, messages.ERROR, _('Kan de zaak niet doorzetten naar de volgende fase.'))
        return redirect('view_case', case.id)

@permission_required('core.can_manage_cases', raise_exception=True)
def change_assignee(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        form = ChangeAssigneeForm(case, instance=case, data=request.POST)
        if form.is_valid():
            case.assignee = form.cleaned_data['assignee']
            case.save()

            case.logs.create(event='change_assignee', performer=request.user.to_dict(), metadata={
                'assignee_name': str(case.assignee) if case.assignee else None
            })

            messages.add_message(request, messages.INFO, _('De behandelaar is gewijzigd.'))
            return redirect('view_case', case.id)
    else:
        form = ChangeAssigneeForm(case, instance=case)

    return render(request, 'cases/change_assignee.html', {
        'case': case,
        'form': form
    })

@permission_required('core.can_manage_cases', raise_exception=True)
def change_phase(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    if request.method == 'POST':
        old_phase = str(case.current_phase) if case.current_phase else None
        form = ChangePhaseForm(case, instance=case, data=request.POST)
        if form.is_valid():
            form.save()

            case.logs.create(event='change_phase', performer=request.user.to_dict(), metadata={
                'old_phase': old_phase,
                'new_phase': str(case.current_phase) if case.current_phase else None,
            })

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

def create_attachment(request, case_id, attachment_type):
    case = get_object_or_404(Case, pk=case_id)

    if case.is_closed:
        messages.add_message(request, messages.ERROR, _('Kan geen bijlage toevoegen aan een gesloten zaak.'))
        return redirect('attachments', case.id)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES, attachment_type=attachment_type)
        if form.is_valid():
            with reversion.create_revision():
                form.save(case=case)
                reversion.set_user(request.user)

            case.logs.create(event='create_attachment', performer=request.user.to_dict())

            return redirect('attachments', case.id)
    else:
        form = AttachmentForm(attachment_type=attachment_type)

    return render(request, 'cases/create_attachment.html', {
        'case': case,
        'form': form,
    })

def delete_attachment(request, case_id, attachment_id):
    case = get_object_or_404(Case, pk=case_id)
    attachment = get_object_or_404(Attachment, pk=attachment_id)

    if case.is_closed:
        messages.add_message(request, messages.ERROR, _('Kan geen bijlage verwijderen van een gesloten zaak.'))
        return redirect('attachments', case.id)

    if request.method == 'POST':
        with reversion.create_revision():
            attachment.delete()
            reversion.set_user(request.user)

        case.logs.create(event='delete_attachment', performer=request.user.to_dict(), metadata={
            'attachment_name': attachment.display_name,
        })

        messages.add_message(request, messages.INFO, _('De bijlage is verwijderd.'))
        return redirect('attachments', case.id)

    return render(request, 'cases/delete_attachment.html', {
        'case': case,
    })

def logs(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    paginator = Paginator(case.logs.all(), 50)

    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    index = page.number - 1
    page_range = paginator.page_range[max(0, index - 5):(min(len(paginator.page_range), index + 5))]

    return render(request, 'cases/logs.html', {
        'case': case,
        'in_logs': True,
        'page_range': page_range,
        'page': page,
    })
