# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from django.contrib.auth import get_user_model

from shuup_multivendor.models import SupplierUser


class CloudSupplierStrategy(object):

    def get_supplier(self, **kwargs):
        suppplier_user = SupplierUser.objects.filter(user=kwargs["user"]).first()
        return (suppplier_user.supplier if suppplier_user else None)


class CloudSupplierUserStrategy(object):

    def get_users(self, **kwargs):
        supplier = kwargs["supplier"]
        user_ids = SupplierUser.objects.filter(supplier=supplier).values_list("user_id", flat=True)
        return get_user_model().objects.filter(id__in=user_ids)
