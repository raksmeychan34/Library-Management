from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    _isbn_unique = models.Constraint(       #database-level rule enforced by Postgres
    'unique(isbn)',
    'ISBN must be unique — this book already exists!',
    )

    active = fields.Boolean(default=True)    #automatically wires up Archive/Unarchive in the Actions menu

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
    is_overdue = fields.Boolean(
    string="Overdue",
    compute="_compute_is_overdue",
    store=True,
    )

    @api.constrains('publish_date')      #Runs auto field changes; raises to block bad data
    def _check_publish_date(self):
        for book in self:
            if book.publish_date and book.publish_date > fields.Date.today():
                raise ValidationError("Publish date cannot be in the future.")       #blocks bad data

    @api.depends('state', 'borrow_date', 'loan_period_days')    #tells Odoo which fields trigger recalculation
    def _compute_is_overdue(self):              #Marks a field as calculated
        today = fields.Date.today()
        for book in self:
            if book.state == 'borrowed' and book.borrow_date:
                due_date = book.borrow_date + timedelta(days=book.loan_period_days)
                book.is_overdue = today > due_date
            else:
                book.is_overdue = False

    def action_borrow(self, borrower_id=None):
        is_librarian = self.env.user.has_group('library_management.group_library_librarian')
        for book in self:
            if book.state == 'borrowed':
                raise UserError(f"'{book.name}' is already borrowed.")
            if not is_librarian and borrower_id != self.env.user.partner_id.id:
                raise UserError("You can only borrow books for yourself.")
            book.sudo().write({
                'state': 'borrowed',
                'borrower_id': borrower_id,
                'borrow_date': fields.Date.today(),
            })
            

    def action_return(self):
        is_librarian =self.env.user.has_group('library_management.group_library_librarian')
        for book in self:
            if not is_librarian and book.borrower_id.id != self.env.user.partner_id.id:
                raise UserError("You can only return books you've borrowed yourself.")
            book.sudo().write({
                'state': 'returned',
                'return_date': fields.Date.today(),
                'borrower_id': False,
            })