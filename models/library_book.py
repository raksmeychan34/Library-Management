from odoo import models, fields
from odoo.exceptions import UserError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    publish_date = fields.Date(string="Publish Date")
    pages = fields.Integer(string="Pages")
    description = fields.Text(string="Description")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
        ],
        string="Status",
        default='draft',
        required=True,
    )

    borrower_id = fields.Many2one('res.partner', string="Borrower")
    borrow_date = fields.Date(string="Borrow Date")
    return_date = fields.Date(string="Return Date")

    def action_borrow(self, borrower_id=None):
        for book in self:
            if book.state == 'borrowed':
                raise UserError(f"'{book.name}' is already borrowed.")
            book.state = 'borrowed'
            book.borrower_id = borrower_id
            book.borrow_date = fields.Date.today()

    def action_return(self):
        for book in self:
            book.state = 'returned'
            book.return_date = fields.Date.today()
            book.borrower_id = False