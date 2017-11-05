"""
webhooks module related views
"""
import hashlib
import hmac
import json
from http import HTTPStatus
from ipaddress import ip_address, ip_network

from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ipware.ip import get_ip

from webhooks.signals import github_event
from zenboard.utils import github_api


class GitHubWebhookReceiverView(View):
    """
    GitHub webhook receiver view.
    """
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Extends Django's `dispatch` method and makes sure that passed
        request is valid and send from GitHub.
        """
        # Make sure request is from GitHub
        request_ip = ip_address(get_ip(request))

        github_meta = github_api.meta()
        whitelisted_subnets = [ip_network(n) for n in github_meta['hooks']]

        for subnet in whitelisted_subnets:
            if request_ip in subnet:
                break
        else:
            return HttpResponseForbidden("Non whitelisted IP")

        # Check signature if GitHub webhook secret is set
        if settings.GITHUB_WEBHOOK_SECRET:
            header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')

            if not header_signature:
                return HttpResponseBadRequest("No signature")

            sha_name, gh_signature = header_signature.split('=')
            if sha_name != 'sha1':
                return HttpResponseBadRequest("Operation not supported")

            signature = hmac.new(
                key=force_bytes(settings.GITHUB_WEBHOOK_SECRET),
                msg=request.body,
                digestmod=hashlib.sha1,
            )
            if not hmac.compare_digest(gh_signature, signature.hexdigest()):
                return HttpResponseForbidden("Invalid signature header")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Receive GitHub event payload and trigger appropriate signal.
        """
        event = request.META.get('HTTP_X_GITHUB_EVENT')
        guid = request.META.get('HTTP_X_GITHUB_DELIVERY')
        payload = json.loads(request.body or '{}')

        github_event.send(
            sender=self.__class__.__name__,
            event=event,
            guid=guid,
            payload=payload,
        )

        return HttpResponse('Webhook received', status=HTTPStatus.OK)
