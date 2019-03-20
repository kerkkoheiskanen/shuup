# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP™ ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import random

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Q
from django.db.transaction import atomic
from django.utils.translation import activate

from shuup.core.models import Order, PersonContact, Product
from shuup_product_reviews_tests.factories import (
    create_random_review_for_product
)


def get_random_reviewer(product):
    """
    Get a random reviewer that didn't review this product yet
    """
    from shuup_product_reviews.models import ProductReview
    return PersonContact.objects.exclude(
        Q(product_reviews__product=product) | Q(user__is_staff=True) | Q(user__is_superuser=True)
    ).order_by("?").first()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--order', type=str, required=True, help="Order ID to generate the review")

    def handle(self, *args, **options):
        activate(settings.PARLER_DEFAULT_LANGUAGE_CODE)
        order_id = options["order"]
        order = Order.objects.get(pk=order_id)
        shop = order.shop

        with atomic():
            # select 50 random products for this shop
            for product in Product.objects.filter(shop_products__shop=shop).order_by("?")[:50]:
                print("Generating reviews for {}-{}".format(product.pk, product))

                # create reviews with comments
                for i in range(random.randint(5, 10)):
                    reviewer = get_random_reviewer(product)
                    create_random_review_for_product(shop, product, order=order, reviewer=reviewer)

                # create reviews without comments
                for i in range(random.randint(5, 10)):
                    reviewer = get_random_reviewer(product)
                    create_random_review_for_product(shop, product, order=order, reviewer=reviewer, generate_comment=False)
