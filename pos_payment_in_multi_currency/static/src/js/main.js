/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_payment_in_multi_currency.pos_payment_in_multi_currency', function(require){
    "use strict";
    var models = require('point_of_sale.models');
  //  var screens = require("point_of_sale.screens");
    var models = require("point_of_sale.models");
    //var gui = require('point_of_sale.gui');
    //var popup_widget = require('point_of_sale.popups');
    var SuperOrder = models.Order.prototype;
    var SuperPaymentline = models.Paymentline.prototype;
    var utils = require('web.utils');
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;
    var field_utils = require('web.field_utils');

    models.load_models([{
        model:'res.currency',
        field: [],
        loaded: function(self, currencies){
            self.currencies = false
            if (self.config.enable_multi_currency && self.config.multi_currency_ids){
                self.currencies = []
                self.currency_by_id = {}
              //  console.log(currencies,self.config.multi_currency_ids)
                _.each(currencies, function(currencie){
                    if(self.config.multi_currency_ids.includes(currencie.id)){
                      if(self.config.currency_id[0] != currencie.id)
                      {
                        self.currencies.push(currencie)
                        self.currency_by_id[currencie.id] = currencie
                      }
                    }
                    if(self.config.currency_id[0] == currencie.id){
                        self.currencies.push(currencie)
                        self.currency_by_id[currencie.id] = currencie
                    }
                    if(currencie.rate == 1){
                        self.base_currency = currencie
                    }
                });
            }

        }
    }], { 'after': 'pos.config' });

    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            var self = this;
            SuperOrder.initialize.call(this, attributes, options);
            self.use_multi_currency = self.use_multi_currency || false;

        },
        init_from_JSON: function (json) {
			var self = this;
			SuperOrder.init_from_JSON.call(this, json);
            this.use_multi_currency = json.use_multi_currency || false;
        },
        export_as_JSON: function () {
			var self = this;
			var loaded = SuperOrder.export_as_JSON.call(this);
			if (self.use_multi_currency)
                loaded.use_multi_currency = self.use_multi_currency;
            return loaded
        },
        get_other_currency_amount(line){
            var self = this;
            //console.log(amt,line.otc_amount);
            if (line && line.currency_id){
                var amt = (self.pos.currency_by_id[line.currency_id].rate*line.otc_amount)/self.pos.currency.rate


                line.other_currency_amount = (self.pos.currency_by_id[line.currency_id].rate*line.get_amount())/self.pos.currency.rate;
                console.log(line.otc_amount,amt)
                return field_utils.format.float(round_di(amt, 4), {digits: [69, 4]})
            } else {
                line.other_currency_amount = 0.0
                return 0.0
            }
        },

        get_change_mc: function(change,paymentline) {
          //console.log(this.use_multi_currency , paymentline , paymentline.other_currency_id)
            if (this.use_multi_currency && paymentline && paymentline.other_currency_id){
                var amt = (this.pos.currency_by_id[paymentline.currency_id].rate*change)/this.pos.currency.rate
                //console.log('amount1',amt,change);
                //amt = parseFloat(field_utils.format.float(round_di(amt, 4), {digits: [69, 4]}));
                amt = parseFloat(round_di(amt, 4));
                //console.log('amount2',amt);
                return amt
            } else {
                return Math.max(0,change);
            }
        },
    });

    models.Paymentline = models.Paymentline.extend({
       initialize: function(attributes, options) {
           var self = this;
           self.other_currency_id = false
           self.other_currency_rate = false
           self.other_currency_amount = 0.0
           self.otc_amount = 0.0
     SuperPaymentline.initialize.call(this, attributes, options);
     self.currency_id = self.currency_id || false;
     self.other_currency_id = self.currency_id || false;
           self.other_currency_rate = self.other_currency_rate || false;
           self.other_currency_amount = self.other_currency_amount || 0.0;
           self.is_multi_currency_payment = self.is_multi_currency_payment || false;
           self.otc_amount = self.otc_amount || 0;
       },
       init_from_JSON: function(json){
           var self = this;
     SuperPaymentline.init_from_JSON.call(this, json);
     self.currency_id = json.currency_id || false;
           self.other_currency_id = self.currency_id || false;
           self.other_currency_rate = json.other_currency_rate || false;
           self.other_currency_amount = self.other_currency_amount || 0.0;
           self.is_multi_currency_payment = json.is_multi_currency_payment || false;
           self.otc_amount = json.otc_amount || 0.0;
       },
       export_as_JSON: function () {
     var self = this;
     var loaded = SuperPaymentline.export_as_JSON.call(self);
     if (self.currency_id){
       loaded.currency_id = self.currency_id;
           }
           if (self.other_currency_id){
       loaded.other_currency_id = self.currency_id;
           }
           if (self.other_currency_rate){
       loaded.other_currency_rate = self.other_currency_rate;
           }
           if (self.other_currency_amount){
       loaded.other_currency_amount = self.other_currency_amount;
           }
           if (self.is_multi_currency_payment){
               loaded.is_multi_currency_payment = self.is_multi_currency_payment
           }
           if (self.otc_amount){
             loaded.otc_amount = self.otc_amount
           }
     return loaded;
       },
   })

});
