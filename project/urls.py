# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP™ ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from django.http import HttpResponseRedirect
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse

from shuup.admin.modules.products.views import ProductMediaBulkAdderView
from shuup.admin.views.dashboard import DashboardView


def not_vendor(view):
    def f(request, *args, **kwargs):
        if getattr(request.user, "is_superuser", False):
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(reverse("shuup_admin:shuup_multivendor.dashboard.supplier"))
    return f


urlpatterns = [
    url(r'^api/', include('shuup.api.urls')),
    url(
        r"^sa/products/(?P<pk>\d+)/media/add/$",
        ProductMediaBulkAdderView.as_view(),
        name="shop_product.add_media_sa"),  # TODO: Revise! Shouldn't be needed.
    url(r'^admin/$', not_vendor(DashboardView.as_view()), name='dashboard'),
    url(r"^admin/", include("shuup.admin.urls", namespace="shuup_admin", app_name="shuup_admin")),
    url(r"^", include("shuup.front.urls", namespace="shuup", app_name="shuup"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
