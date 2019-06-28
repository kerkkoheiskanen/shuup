# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from shuup.admin.modules.products.views import ProductMediaBulkAdderView
from shuup.admin.views.dashboard import DashboardView
from shuup.core.utils.maintenance import maintenance_mode_exempt


def not_vendor(view):
    def f(request, *args, **kwargs):
        user = request.user
        is_superuser = getattr(user, "is_superuser", False)
        is_staff_member = request.shop and request.shop.staff_members.filter(id=user.id).exists()
        if is_superuser or is_staff_member:
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(reverse("shuup_admin:shuup_multivendor.dashboard.supplier"))
    return f


urlpatterns = [
    url(r'^api/', include('shuup.api.urls')),
    url(
        r"^sa/products/(?P<pk>\d+)/media/add/$",
        ProductMediaBulkAdderView.as_view(),
        name="shop_product.add_media_sa"),  # TODO: Revise! Shouldn't be needed.
    url(r'^admin/$', maintenance_mode_exempt(not_vendor(DashboardView.as_view())), name='dashboard'),
    url(r"^admin/", include("shuup.admin.urls", namespace="shuup_admin", app_name="shuup_admin")),
    url(r"^", include("shuup.front.urls", namespace="shuup", app_name="shuup"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
