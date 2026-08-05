from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    borrowed_book_count = fields.Integer(
        string="Borrowed Books",
        compute='_compute_borrowed_book_count',
    )

    def _compute_borrowed_book_count(self):
        for partner in self:
            partner.borrowed_book_count = self.env['library.book'].search_count([
                ('borrower_id', '=', partner.id),
                ('state', '=', 'borrowed'),
            ])