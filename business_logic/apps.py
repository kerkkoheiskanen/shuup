# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "business_logic"
    verbose_name = "Business Logic"
    label = "business_logic"
    provides = {}

    def ready(self):
        import business_logic.logging  # noqa
