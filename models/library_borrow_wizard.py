from odoo import models, fields, api
from odoo.fields import Command


class LibraryBorrowWizard(models.TransientModel):
    _name = 'library.borrow.wizard'
    _description = 'Borrow Book Wizard'

    book_ids = fields.Many2many('library.book', string="Books", required=True)
    borrower_id = fields.Many2one('res.partner', string="Borrower", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            res['book_ids'] = [Command.set(active_ids)]
        return res

    def action_confirm_borrow(self):
        for book in self.book_ids:
            book.action_borrow(borrower_id=self.borrower_id.id)