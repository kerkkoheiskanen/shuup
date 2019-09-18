# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from __future__ import unicode_literals

import logging

from django.conf import settings

from shuup.notify.models import Script
from shuup.notify.script import Context

from .signals import notification_sent

LOG = logging.getLogger(__name__)


def run_event(event, shop):
    for script in Script.objects.filter(event_identifier=event.identifier, enabled=True):
        try:
            notification_sent.send(sender=Script, script=script, event=event, shop=shop)
            script.execute(context=Context.from_event(event, shop))
        except Exception:  # pragma: no cover
            if settings.DEBUG:
                raise
            LOG.exception("Script %r failed for event %r" % (script, event))
