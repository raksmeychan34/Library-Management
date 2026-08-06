from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    _isbn_unique = models.Constraint(
    'unique(isbn)',
    'ISBN must be unique — this book already exists!',
    )

    active = fields.Boolean(default=True)

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

    loan_period_days = fields.Integer(string="Loan Period (days)", default=14)
    is_overdue = fields.Boolean(string="Overdue", compute='_compute_is_overdue')

    @api.constrains('publish_date')
    def _check_publish_date(self):
        for book in self:
            if book.publish_date and book.publish_date > fields.Date.today():
                raise ValidationError("Publish date cannot be in the future.")

    @api.depends('state', 'borrow_date', 'loan_period_days')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for book in self:
            if book.state == 'borrowed' and book.borrow_date:
                due_date = book.borrow_date + timedelta(days=book.loan_period_days)
                book.is_overdue = today > due_date
            else:
                book.is_overdue = False

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