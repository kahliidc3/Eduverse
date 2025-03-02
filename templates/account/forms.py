from django.forms.renderers import TemplatesSetting

class FormRenderer(TemplatesSetting):
    form_template_name = "account/forms/form.html"
    formset_template_name = "account/forms/formset.html"
    field_template_name = "account/forms/field.html"
