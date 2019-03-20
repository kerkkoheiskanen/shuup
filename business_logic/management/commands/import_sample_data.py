# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import os
import random
from decimal import Decimal

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.translation import activate

from shuup.core.models import (
    CustomCarrier, CustomPaymentProcessor, FixedCostBehaviorComponent,
    PaymentMethod, ShippingMethod, Shop, ShopProduct, Supplier, TaxClass
)
from shuup_multivendor.models import SupplierPrice
from shuup_us_taxes.importer import TaxImporter
from shuup_yaml.importer import (
    import_categories, import_manufacturers, import_products
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        activate(settings.PARLER_DEFAULT_LANGUAGE_CODE)
        main_shop = Shop.objects.get(identifier="main_store")

        importer = TaxImporter()
        importer.import_taxes()

        tax_class = TaxClass.objects.first()
        create_payment_methods([main_shop], tax_class)
        create_shipping_methods([main_shop], tax_class)

        this_dir = os.path.dirname(__file__)
        data_path = os.path.realpath(os.path.join(this_dir, "..", "..", "..", "..", "data"))
        if not os.path.exists(data_path):
            return

        img_path = os.path.realpath(os.path.join(this_dir, "..", "..", "..", "..", "data", "images")) + "/"
        print("Importing manufacturers...")
        import_manufacturers(main_shop, os.path.join(data_path, "manufacturers.yaml"), img_path)
        print("Importing categories...")
        import_categories(main_shop, os.path.join(data_path, "categories.yaml"))
        print("Importing products...")
        import_products(main_shop, os.path.join(data_path, "products.yaml"), img_path, tax_class)

        print("Generating supplier data...")
        for shop_product in ShopProduct.objects.filter(shop=main_shop):
            generate_supplier_prices(shop_product)


def create_payment_methods(shops, tax_class):
    processor = CustomPaymentProcessor.objects.create()
    for shop in shops:
        # processor = CustomPaymentProcessor.objects.create()
        cash_method, _ = PaymentMethod.objects.get_or_create(
            shop=shop,
            defaults=dict(
            payment_processor=processor,
            choice_identifier="cash",
            tax_class=tax_class, name="Cash", enabled=True))

        shop_products = ShopProduct.objects.filter(shop=shop)
        for sp in shop_products:
            sp.payment_methods.set([cash_method])


def create_shipping_methods(shops, tax_class):
    carrier = CustomCarrier.objects.update_or_create(identifier="default_carrier", defaults=dict(name="Default"))[0]
    for shop in shops:
        shipping_method, _ = ShippingMethod.objects.get_or_create(
            identifier="%s-%s" % (shop.id, "default_identifier"),
            shop_id=shop.id,
            defaults=dict(
                carrier_id=carrier.id,
                choice_identifier=carrier.get_service_choices()[0].identifier,
                tax_class_id=tax_class.id,
                name="Manual shipping"
            ))

        shipping_method.enabled = True
        shipping_method.save()

        if not shipping_method.behavior_components.instance_of(FixedCostBehaviorComponent).exists():
            price = Decimal("0.0")
            behavior_component = FixedCostBehaviorComponent.objects.create(price_value=price)
            behavior_component.name = shipping_method.name
            behavior_component.save()
            shipping_method.behavior_components.add(behavior_component)

        shop_products = ShopProduct.objects.filter(shop=shop)
        for sp in shop_products:
            sp.shipping_methods.set([shipping_method])


def generate_supplier_prices(shop_product):
    """
    Each product now has first supplier as supplier so let's
    shuffle those suppliers a little bit. Also let's set random
    price for each supplier which is slightly above product
    default price.
    """
    shop_product.suppliers.clear()
    supplier_query = Supplier.objects.filter(shops=shop_product.shop, module_identifier="simple_supplier")
    for supplier in supplier_query.order_by("?")[:random.randint(0, 7)]:
        shop_product.suppliers.add(supplier)

        profit = Decimal(1) + Decimal(random.randint(1, 75) / 100)
        supplier_price_value = shop_product.default_price_value * profit
        SupplierPrice.objects.update_or_create(
            shop=shop_product.shop, supplier=supplier, product=shop_product.product,
            defaults=dict(amount_value=supplier_price_value))

        target_stock_count = random.randint(100, 300)
        product = shop_product.product
        logical_count = supplier.get_stock_status(product.pk).logical_count
        supplier.adjust_stock(product.id, target_stock_count - logical_count)
