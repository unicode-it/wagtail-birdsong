from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.module_loading import import_string
from django.views.generic.edit import FormView
from wagtail.models import Site

from birdsong.conf import BIRDSONG_DOUBLE_OPT_IN_ENABLED
from birdsong.forms import ContactForm
from birdsong.models import Contact, DoubleOptInSettings
from birdsong.views import actions


class SignUpView(FormView):
    template_name = "site/signup.html"
    form_class = ContactForm
    contact_model = Contact

    def form_valid(self, form):
        if BIRDSONG_DOUBLE_OPT_IN_ENABLED == True: 
            from birdsong.options import BIRDSONG_DEFAULT_BACKEND

            double_opt_in_settings = DoubleOptInSettings.load(request_or_site=self.request)
            contact, created = self.contact_model.objects.get_or_create(email=form.cleaned_data["email"])

            site = Site.find_for_request(self.request)
            url = (
                site.root_url
                + reverse("birdsong:confirm", args=[contact.token])
            )

            backend_class = import_string(
                getattr(settings, "BIRDSONG_BACKEND", BIRDSONG_DEFAULT_BACKEND)
            )

            actions.send_confirmation(backend_class(), self.request, contact, url)

            redirect_url = "/"
            if double_opt_in_settings.campaign_signup_redirect:
                redirect_url = double_opt_in_settings.campaign_signup_redirect.get_url()

            return redirect(redirect_url)
