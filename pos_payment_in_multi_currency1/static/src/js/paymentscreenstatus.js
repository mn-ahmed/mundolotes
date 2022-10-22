/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_payment_in_multi_currency.pos_payment_in_multi_currency_screen_status', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    var PaymentScreenStatus = require("point_of_sale.PaymentScreenStatus");
    var field_utils = require('web.field_utils');
    const { useListener } = require('web.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
const Registries = require('point_of_sale.Registries');
var utils = require('web.utils');
var round_di = utils.round_decimals;
    const posPaymentScreenStatus = (PaymentScreenStatus) =>
    class extends PaymentScreenStatus{
      formating(amount,currency_id){
        if(currency_id){
          var currency = this.env.pos.currency_by_id[currency_id];
        }
        else{
          var currency = this.env.pos.currency;
        }
        //console.log(this.env.pos.currency)
        if (currency.position === 'after') {
            return amount + ' ' + (currency.symbol || '');
        } else {
            return (currency.symbol || '') + ' ' + amount;
        }
      }
    format_currency_n_symbol(amount,precisson){
        if (typeof amount === 'number') {
         var decimals = 4;
        amount = round_di(amount, decimals).toFixed(decimals);
              amount = field_utils.format.float(round_di(amount, decimals), {
                  digits: [69, decimals],});
                }
                return amount;

      }
      get changeTextmc() {
        console.log("am",this.currentOrder.get_change())
         if(this.env.pos.config.enable_multi_currency && this.currentOrder.use_multi_currency){
        //   console.log(this.currentOrder.get_change(this.currentOrder.selected_paymentline))
           var amt = this.format_currency_n_symbol(
           this.currentOrder.get_change_mc(this.currentOrder.get_change(),this.currentOrder.selected_paymentline),0.0001);
           var currency_id = this.currentOrder.selected_paymentline.other_currency_id;

          return this.formating(amt,currency_id)
         }
         else{
           return this.env.pos.format_currency(this.currentOrder.get_change());
         }
       }
       get totalDueTextmc() {
         if(this.env.pos.config.enable_multi_currency && this.currentOrder.use_multi_currency){
            var currency_id = this.currentOrder.selected_paymentline.other_currency_id;
            //var due= parseFloat(this.currentOrder.get_due(this.currentOrder.selected_paymentline).replace(',',''))
            var due = this.currentOrder.get_change_mc(this.currentOrder.get_total_with_tax() + this.currentOrder.get_rounding_applied(),this.currentOrder.selected_paymentline)
        var amt = this.format_currency_n_symbol(
          due >0 ? due : 0,0.0001);
          //console.log(amt,)
          return this.formating(amt,currency_id)
         }
         else{
           return this.format_currency(
               this.currentOrder.get_total_with_tax() + this.currentOrder.get_rounding_applied()
           );
         }
       }
       get remainingTextmc() {
         if(this.env.pos.config.enable_multi_currency && this.currentOrder.use_multi_currency){
            var currency_id = this.currentOrder.selected_paymentline.other_currency_id;
            //var rem = parseFloat(this.currentOrder.get_due(this.currentOrder.selected_paymentline).replace(',','')) - parseFloat(this.currentOrder.get_other_currency_amount(this.currentOrder.selected_paymentline).replace(',',''))
            var rem = this.currentOrder.get_change_mc(this.currentOrder.get_due(),this.currentOrder.selected_paymentline)
            var amt =  this.format_currency_n_symbol(
      rem > 0 ? rem : 0      ,0.0001)
            return this.formating(amt,currency_id)
                   }
         else{
           return this.env.pos.format_currency(
               this.currentOrder.get_due() > 0 ? this.currentOrder.get_due() : 0
           );
         }
       }
       get convamount(){
         return this.env.pos.format_currency_no_symbol(this.currentOrder.selected_paymentline.get_amount());
       }



};
Registries.Component.extend(PaymentScreenStatus, posPaymentScreenStatus);

    return PaymentScreenStatus;
});
