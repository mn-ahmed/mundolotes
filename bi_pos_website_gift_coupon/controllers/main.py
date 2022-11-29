# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


import werkzeug
import odoo
from odoo import addons
from odoo import models, fields, api
from odoo import SUPERUSER_ID
from odoo import http, tools, _
from odoo.http import request
from odoo.tools.translate import _
import odoo.http as http
from odoo.http import request
from datetime import datetime, timedelta

import werkzeug.urls
import werkzeug.wrappers
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

	@http.route(['/gift/coupon'], type='http', auth="public", website=True, sitemap=False)
	def voucher_code(self, coupon, **post):

		redirect = post.get('r', '/shop/cart')

		current_sale_order = request.website.sale_get_order()

		for i in  current_sale_order.order_line:
			if i.discount_line == True:
				return request.redirect("%s?coupon_not_available=A Voucher is already applied. Please remove it from cart to apply new Voucher." % redirect)
		dv = False
		by_name = request.env['pos.gift.coupon'].search([('name', '=ilike', coupon)])
		by_code = request.env['pos.gift.coupon'].search([('c_barcode','=', coupon)])
		if by_name:
			dv = by_name
		if by_code:
			dv = by_code
		if not dv:
			return request.redirect("%s?coupon_not_available=Invalid Voucher !" % redirect)
		else:   
			dv = request.env['pos.gift.coupon'].browse(dv).id
			dt_end = False
			discount_value = False
			order_line_obj = request.env['sale.order.line'].sudo()
			
			if dv.coupon_count > dv.coupon_apply_times :
				return request.redirect("%s?coupon_not_available=Can not use coupon because you reached the maximum limit of usage." % redirect)

			if dv.amount_type == 'fix':
				for i in current_sale_order.order_line:
					if i.discount_line == False:
						if dv.products_true or dv.is_categ:
							if dv.products_true:
								if i.product_id in dv.product_ids:
									discount_value =  dv.amount
							if dv.is_categ:
								if (i.product_id not in dv.product_ids) and (i.product_id.public_categ_ids in dv.ecommerce_category_ids):
									discount_value =  dv.amount
						else:
							discount_value =  dv.amount

			elif dv.amount_type == 'per':
				total = 0
				for i in current_sale_order.order_line:
					if i.discount_line == False:
						if dv.products_true or dv.is_categ:
							if dv.products_true:
								if i.product_id in dv.product_ids:
									total += i.price_subtotal
							if dv.is_categ:
									if (i.product_id not in dv.product_ids) and (i.product_id.public_categ_ids in dv.ecommerce_category_ids):
										total += i.price_subtotal
						else:
							total += i.price_subtotal
				discount_value = ((total * dv.amount)/100)

			if discount_value <= 0:
				return request.redirect("%s?coupon_not_available=None of the cart product is applicable to get discount with this coupon." % redirect)

			if dv.exp_dat_show:
				dt_end = datetime.strptime(str(dv.expiry_date), '%Y-%m-%d %H:%M:%S').date()

			if not dv.max_amount >= discount_value:
				return request.redirect("%s?coupon_not_available=Discount amount is higher than maximum amount of this coupon." % redirect)


			if not current_sale_order.amount_total >= discount_value:
				return request.redirect("%s?coupon_not_available=Can not apply discount more than order total." % redirect)

			if dv.partner_true == True:
				partner = dv.partner_id.id
				curr_user_partner = request.env['res.users'].browse(request._uid).partner_id
				selected_partner = request.env['res.partner'].browse(partner)
				
				flag = False
				if curr_user_partner.id == selected_partner.id:
					if dv.exp_dat_show:
						if dt_end < datetime.now().date():
							return request.redirect("%s?coupon_not_available=This code has been Expired" % redirect)
					res = order_line_obj.sudo().create({
							'product_id': dv.product_id.id,
							'name': dv.product_id.name,
							'price_unit': -discount_value,
							'order_id': current_sale_order.id,
							'product_uom':dv.product_id.uom_id.id,
							'discount_line':True,
					})
					current_sale_order.sale_coupon_id = dv
					current_sale_order.assign_voucher_code(coupon)
					return request.redirect(redirect)
				else:
					return request.redirect("%s?coupon_not_available=Invalid Customer !" % redirect)

			if dv.exp_dat_show:
				if dt_end < datetime.now().date():
					return request.redirect("%s?coupon_not_available=This code has been Expired" % redirect)

			res = order_line_obj.sudo().create({
				'product_id': dv.product_id.id,
				'name': dv.product_id.name,
				'price_unit': -discount_value,
				'order_id': current_sale_order.id,
				'product_uom':dv.product_id.uom_id.id,
				'discount_line':True,
			})
			current_sale_order.sale_coupon_id = dv
			current_sale_order.assign_voucher_code(coupon) 
		
		return request.redirect(redirect)


	@http.route('/shop/payment/validate', type='http', auth="public", website=True)
	def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
		""" Method that should be called by the server when receiving an update
		for a transaction. State at this point :

		 - UDPATE ME

		"""
		if sale_order_id is None:
			order = request.website.sale_get_order()
		else:
			order = request.env['sale.order'].sudo().browse(sale_order_id)
			assert order.id == request.session.get('sale_last_order_id')

		if transaction_id:
			tx = request.env['payment.transaction'].sudo().browse(transaction_id)
			assert tx in order.transaction_ids()
		elif order:
			tx = order.get_portal_last_transaction()
		else:
			tx = None

		if not order or (order.amount_total and not tx):
			return request.redirect('/shop')

		list_of_order_product = []
		voucher_id = False

		if order.voucher_code:
			voucher_obj_by_name = request.env['pos.gift.coupon'].search([('name', '=ilike', order.voucher_code)])
			voucher_obj_by_code = request.env['pos.gift.coupon'].search([('c_barcode', '=', order.voucher_code)])
			if voucher_obj_by_name:
				dic = {'code':voucher_obj_by_name,'order':order}
				self._apply_coupon(dic)

			if voucher_obj_by_code:
				dic = {'code':voucher_obj_by_code,'order':order}
				self._apply_coupon(dic)

		if (not order.amount_total and not tx) or tx.state in ['pending', 'done', 'authorized']:
			if (not order.amount_total and not tx):
				# Orders are confirmed by payment transactions, but there is none for free orders,
				# (e.g. free events), so confirm immediately
				order.with_context(send_email=True).action_confirm()
		elif tx and tx.state == 'cancel':
			# cancel the quotation
			order.action_cancel()

		# clean context and session, then redirect to the confirmation page
		request.website.sale_reset()
		if tx and tx.state == 'draft':
			return request.redirect('/shop')

		return request.redirect('/shop/confirmation')

	def _apply_coupon(self,arg):
		partner_record_id = request.env['res.users'].browse(request._uid).partner_id.id
		coupon = arg['code']
		order = arg['order']
		discount_value = 0
		if coupon.amount_type == 'fix':
				discount_value = coupon.amount
		elif coupon.amount_type == 'per':
			total = 0
			for i in order.order_line:
				if i.discount_line == False:
					total += i.price_subtotal
			discount_value = ((total * coupon.amount)/100)
		coupon.update({
			'coupon_count': (coupon.coupon_count + 1),
			'max_amount':coupon.max_amount - discount_value,
		})
		order.write({
			'sale_coupon_id': coupon.id
		})
		used_sale_coup_id = coupon.sudo().sale_order_ids.sudo().browse(order.id).sale_coupon_id.id
		curr_vouch_id = coupon.id

		if used_sale_coup_id == curr_vouch_id:
			coupon.sale_order_ids.sudo().update({
				'user_id': http.request.env.context.get('uid'),
			})

