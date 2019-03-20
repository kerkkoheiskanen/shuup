# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import random
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import BaseCommand
from django.utils.text import slugify
from django.utils.translation import activate

from shuup.core.models import (
    get_person_contact, Shop, ShopProduct, Supplier
)
from shuup_multivendor.models import SupplierPrice, SupplierUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help="Supplier name")

    def handle(self, *args, **options):
        activate(settings.PARLER_DEFAULT_LANGUAGE_CODE)

        main_shop = Shop.objects.get(identifier="main_store")
        vendor_group, _ = Group.objects.get_or_create(name=settings.VENDORS_PERMISSION_GROUP_NAME)

        name = options["name"]
        identifier = slugify(name)

        print("Creating supplier %s..." % name)
        supplier, _ = Supplier.objects.update_or_create(identifier=identifier, defaults=dict(
            name=name, stock_managed=True, module_identifier="simple_supplier", enabled=True
        ))
        supplier.shops.set([main_shop])

        email = "%s@example.com" % identifier
        username = password = "%s" % identifier
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
        user.groups.add(vendor_group)

        SupplierUser.objects.get_or_create(shop=main_shop, supplier=supplier, user=user)

        contact = get_person_contact(user)
        contact.shops.set([main_shop])

        for shop_product in ShopProduct.objects.all().order_by("?")[:50]:
            shop_product.suppliers.add(supplier)

            profit = Decimal(1) + Decimal(random.randint(1, 75) / 100)
            supplier_price_value = shop_product.default_price_value * profit
            print("%s starting so sell product %s with price %s" % (
                supplier.name, shop_product.product.name, supplier_price_value)
            )
            SupplierPrice.objects.update_or_create(
                shop=shop_product.shop, supplier=supplier, product=shop_product.product,
                defaults=dict(amount_value=supplier_price_value))

            target_stock_count = random.randint(100, 300)
            product = shop_product.product
            logical_count = supplier.get_stock_status(product.pk).logical_count
            supplier.adjust_stock(product.id, target_stock_count - logical_count)
