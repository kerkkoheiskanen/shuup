# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import BaseCommand, call_command
from django.utils.translation import activate

from shuup import configuration
from shuup.core.defaults.order_statuses import create_default_order_statuses
from shuup.core.models import (
    get_person_contact, ProductType, SalesUnit, Shop, ShopStatus, Supplier
)
from shuup.xtheme import set_current_theme
from shuup_multivendor.models import SupplierUser
from shuup_multivendor.utils.permissions import (
    ensure_staff_permission_group_permissions,
    ensure_vendor_permission_group_permissions
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        activate(settings.PARLER_DEFAULT_LANGUAGE_CODE)

        create_default_order_statuses()

        ProductType.objects.update_or_create(identifier="default", defaults=dict(
            name="Standard Product"
        ))
        SalesUnit.objects.update_or_create(identifier="pcs", defaults=dict(
            name="Pieces", symbol="pcs"
        ))

        # Create main shop
        main_shop, _ = Shop.objects.update_or_create(identifier="main_store", defaults=dict(
            name="Main Store",
            public_name="Main Store",
            domain="sandbox",
            currency="USD",
            maintenance_mode=False,
            status=ShopStatus.ENABLED
        ))
        set_current_theme("shuup.themes.classic_gray", main_shop)

        # Create admin user
        admin_user, _ = User.objects.update_or_create(email="admin@example.com", username="admin", defaults=dict(
            first_name="Admin",
            last_name="Superuser",
            is_staff=True,
            is_active=True,
            is_superuser=True
        ))
        admin_user.set_password("admin")
        admin_user.save()

        staff1, _ = User.objects.update_or_create(username="staff1", defaults=dict(
            email="staff1@example.com",
            first_name="First",
            last_name="Staff",
            is_staff=True,
            is_active=True
        ))
        staff1.set_password("staff1")
        staff1.save()

        staff2, _ = User.objects.update_or_create(username="staff2", defaults=dict(
            email="staff2@example.com",
            first_name="Second",
            last_name="Staff",
            is_staff=True,
            is_active=True
        ))
        staff2.set_password("staff2")
        staff2.save()

        main_shop.staff_members.add(staff1)
        main_shop.staff_members.add(staff2)

        staff_group, _ = Group.objects.get_or_create(name=settings.STAFF_PERMISSION_GROUP_NAME)
        staff1.groups.add(staff_group)
        staff2.groups.add(staff_group)

        configuration.set(main_shop, "staff_user_permission_group", staff_group.pk)
        staff_group.permissions.clear()
        ensure_staff_permission_group_permissions(staff_group)

        users = []
        for x in range(0, 10):
            identifier = "vendor%s" % x
            name = "Vendor %s" % x

            supplier, _ = Supplier.objects.update_or_create(identifier=identifier, defaults=dict(
                name=name, stock_managed=True, module_identifier="simple_supplier", enabled=True
            ))
            supplier.shops.set([main_shop])

            email = "vendor%s@example.com" % x
            username = password = "vendor%s" % x
            first_name = "John"
            last_name = "Doe"

            user, _ = User.objects.update_or_create(email=email, username=username, defaults=dict(
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_active=True
            ))
            user.set_password(password)
            user.save()
            users.append(user)

            SupplierUser.objects.get_or_create(shop=main_shop, supplier=supplier, user=user)

            contact = get_person_contact(user)
            contact.shops.set([main_shop])

        # Setup vendor permissions
        vendor_group, _ = Group.objects.get_or_create(name=settings.VENDORS_PERMISSION_GROUP_NAME)
        vendor_group.permissions.clear()
        configuration.set(main_shop, "vendor_user_permission_group", vendor_group.pk)
        ensure_vendor_permission_group_permissions(vendor_group)

        for user in users:
            user.groups.add(vendor_group)
