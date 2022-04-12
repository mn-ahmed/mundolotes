from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class DeliverySlipSummarized(models.AbstractModel):
    _name = 'report.stock_ext.report_deliveryslip_summarized'
    _description = 'Report Delivery Slip Summarized'

    @api.model
    def _get_report_values(self, docids, data=None):
        if docids and len(docids)>1:
            raise UserError(_("Delivery Slip (Summarised) report can only be generated from the form view.\nTip: Open the record and the print the report."))
        docs = self.env['stock.picking'].browse(docids)

        gby_product_categ_ids = self.env['stock.move.line'].read_group(
            domain=[
                ('id', 'in', docs.move_line_ids_without_package.ids),
            ],
            fields=['stock_move_line_ids:array_agg(id)','count_lot_id:count(lot_id)', 'sum_qty_done:sum(qty_done)','sum_qty_done_amount:sum(qty_done_amount)'],
            groupby=['product_categ_id'],
            offset=0,
            limit=None,
            orderby=False,
            lazy=False
        )
        category_dicts = {}
        for gby_product_categ_id in gby_product_categ_ids:
            gby_product_categ_id__product_categ_id = gby_product_categ_id['product_categ_id']
            gby_product_categ_id__stock_move_line_ids = gby_product_categ_id['stock_move_line_ids']
            gby_product_categ_id__count_lot_id = gby_product_categ_id['count_lot_id']
            gby_product_categ_id__sum_qty_done = gby_product_categ_id['sum_qty_done']
            gby_product_categ_id__sum_qty_done_amount = gby_product_categ_id['sum_qty_done_amount']

            category_dicts[gby_product_categ_id__product_categ_id[1]] = {}
            category_dicts[gby_product_categ_id__product_categ_id[1]]['internal_reference_dicts'] = []
            category_dicts[gby_product_categ_id__product_categ_id[1]]['category_count_lot_id'] = gby_product_categ_id__count_lot_id
            category_dicts[gby_product_categ_id__product_categ_id[1]]['category_sum_qty_done'] = gby_product_categ_id__sum_qty_done
            category_dicts[gby_product_categ_id__product_categ_id[1]]['category_sum_qty_done_amount'] = gby_product_categ_id__sum_qty_done_amount

            # product_categ_id = self.env['product.category'].browse(g__product_categ_id)
            gby_internal_references = self.env['stock.move.line'].read_group(
                domain=[
                    ('id', 'in', gby_product_categ_id__stock_move_line_ids),
                ],
                fields=['stock_move_line_ids:array_agg(id)', 'count_lot_id:count(lot_id)', 'sum_qty_done:sum(qty_done)', 'sum_qty_done_amount:sum(qty_done_amount)', ],
                groupby=['product_id_default_code'],
                offset=0,
                limit=None,
                orderby=False,
                lazy=False
            )
            internal_reference_dict = {}
            for gby_internal_reference in gby_internal_references:
                internal_reference_dict['product_id_default_code'] = gby_internal_reference['product_id_default_code']
                internal_reference_dict['count_lot_id'] = gby_internal_reference['count_lot_id']
                internal_reference_dict['sum_qty_done'] = gby_internal_reference['sum_qty_done']
                internal_reference_dict['sum_qty_done_amount'] = gby_internal_reference['sum_qty_done_amount']

                category_dicts[gby_product_categ_id__product_categ_id[1]]['internal_reference_dicts'].append(internal_reference_dict.copy())
                internal_reference_dict.clear()


        report = self.env['ir.actions.report']._get_report_from_name('stock_ext.report_deliveryslip_summarized')

        docargs = {
            'doc_ids': docids,
            'docs': docs,
            'category_dicts': category_dicts,
            'doc_model': report.model,
            # 'data': data,
        }

        return docargs