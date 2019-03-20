# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP™ ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from shuup.front.checkout import VerticalCheckoutProcess
from shuup.front.views.checkout import CheckoutViewWithLoginAndRegister


class CheckoutViewWithLoginAndRegisterVertical(CheckoutViewWithLoginAndRegister):
    process_class = VerticalCheckoutProcess
