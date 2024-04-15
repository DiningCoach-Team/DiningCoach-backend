from django.contrib.sites.shortcuts import get_current_site

from user.tasks import password_reset_send_email

from allauth.account.adapter import *
from allauth.account.utils import user_field


class CustomUserAccountAdapter(DefaultAccountAdapter):
  def save_user(self, request, user, form, commit=True):
    user = super().save_user(request, user, form, commit)

    platform_type = form.PLATFORM_TYPE
    if platform_type:
      user_field(user, 'platform_type', platform_type)

    platform_id = form.PLATFORM_ID
    if platform_id:
      user_field(user, 'platform_id', platform_id)

    user_agent = self.get_http_user_agent(request)
    if user_agent:
      user_field(user, 'user_agent', user_agent)

    user.save()
    return user

  def send_mail(self, template_prefix, email, context):
    ctx = {
      'email': email,
      'current_site': get_current_site(globals()['context'].request),
    }
    ctx.update(context)

    msg = self.render_mail(template_prefix, email, ctx)
    password_reset_send_email.apply_async(kwargs={'msg': msg}, serializer='pickle')
