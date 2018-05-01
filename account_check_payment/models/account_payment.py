# -*- coding: utf-8 -*-
##############################################################################
#
#   Check Payment
#   Authors: Dominador B. Ramos Jr. <mongramosjr@gmail.com>
#   Company: Basement720 Technology Inc.
#
#   Copyright 2018 Dominador B. Ramos Jr.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################
import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class AccountRegisterPayments(models.TransientModel):
    _inherit = "account.register.payments"
    
    check_payment_transaction_ids = fields.One2many('check.payment.transaction', 'account_payment_id', string="Check Information",
        readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    hide_check_payment = fields.Boolean(compute='_compute_hide_check_payment',
        help="Technical field used to hide the check_payment if the selected journal has not been set or the selected journal has a type neither in in bank nor cash")
        
    check_payment_transaction_ids = fields.One2many('check.payment.transaction', 'account_payment_id', string="Check Information",
        readonly=True, states={'draft': [('readonly', False)]}, copy=False)


    @api.multi
    @api.depends('journal_id')
    def _compute_hide_check_payment(self):
        for payment in self:
            if not payment.journal_id:
                payment.hide_check_payment = True
                continue
            if payment.journal_id.type == 'bank' or payment.journal_id.type == 'cash':
                payment.hide_check_payment = False
            else:
                payment.hide_check_payment = True
