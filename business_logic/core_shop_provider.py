# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP™ ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from shuup.core.models import Shop


class DefaultShopProvider(object):
    @classmethod
    def get_shop(cls, request, **kwargs):
        shop = getattr(request, "_cached_default_shop_provider_shop", None)
        if shop:
            return shop

        shop = Shop.objects.first()
        # cache shop as we already calculated it
        setattr(request, "_cached_default_shop_provider_shop", shop)
        return shop
