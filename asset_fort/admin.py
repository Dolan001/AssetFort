from django.contrib import admin

from django.apps import apps


app_models = apps.get_app_config('asset_fort').get_models()

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != 'description']
        self.exclude = ['slug']
        super(ListAdminMixin, self).__init__(model, admin_site)


for model in app_models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
