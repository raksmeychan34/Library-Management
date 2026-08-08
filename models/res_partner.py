from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.One2many(
        'library.book',
        'borrower_id',
        string='Books'
    )

    borrowed_book_count = fields.Integer(
        string="Borrowed Books",
        compute='_compute_borrowed_book_count',
    )

    def _compute_borrowed_book_count(self):
        for partner in self:
            partner.borrowed_book_count = len(
                partner.book_ids.filtered(
                    lambda b: b.state == 'borrowed'
                )
            )