# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Pos Multi Currency",
  "summary"              :  """Pos Multi Currency provide a multi-currency facility to your customers in POS""",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """Pos Multi Currency
  Multiple Currencies
  Foreign Currency
  Exchange Money
  Payment Multi-Currency
  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_payment_in_multi_currency&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  ['views/pos_config.xml',],
  "assets"               :  {
                              'point_of_sale.assets': [
                                "/pos_payment_in_multi_currency/static/src/js/main.js",
                                "/pos_payment_in_multi_currency/static/src/js/paymentscreen.js",
                                "/pos_payment_in_multi_currency/static/src/js/PopupWidget.js",
                                "/pos_payment_in_multi_currency/static/src/js/paymentscreenpaymentlines.js",
                                "/pos_payment_in_multi_currency/static/src/js/paymentscreenstatus.js",
                                "/pos_payment_in_multi_currency/static/src/css/pos.css",
                              ],
                              'web.assets_qweb': [
                                'pos_payment_in_multi_currency/static/src/xml/**/*',
                              ],
                            },
  "demo"                 :  ['demo/demo.xml',],
  "images"               :  ['static/description/banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  149,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
