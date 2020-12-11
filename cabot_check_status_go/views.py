from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cabot.cabotapp.models import StatusCheck
from cabot.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import StatusGoStatusCheck


class StatusGoStatusCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')

    class Meta:
        model = StatusGoStatusCheck
        fields = (
            'name',
            'node_type',
            'enode',
            'timeout',
            'frequency',
            'active',
            'importance',
            'debounce',
        )

        widgets = dict(**base_widgets)
        widgets.update({
            'node_type': forms.Select(attrs={
                'data-rel': 'chosen',
            }),
            'enode': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'enode://123qwe@10.1.2.3:30303',
            }),
        })


class StatusGoCheckCreateView(CheckCreateView):
    model = StatusGoStatusCheck
    form_class = StatusGoStatusCheckForm


class StatusGoCheckUpdateView(CheckUpdateView):
    model = StatusGoStatusCheck
    form_class = StatusGoStatusCheckForm


def duplicate_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-statusgo-check', kwargs={'pk': npk}))
