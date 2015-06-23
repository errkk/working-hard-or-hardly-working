from django import forms


class WorkplaceForm(forms.Form):
    workplace = forms.ChoiceField(required=False)

    def __init__(self, places=None, *args, **kwargs):
        super(WorkplaceForm, self).__init__(self, *args, **kwargs)
        #if places:
            #self.fields['workplace'].choices = places
