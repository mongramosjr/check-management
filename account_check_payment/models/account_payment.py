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

    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        res = super(AccountPayment, self)._onchange_amount()
        if self.payment_type == 'transfer':
            self.hide_check_payment = True
        elif self.payment_type == 'outbound' or self.payment_type == 'inbound':
            if self.journal_id.type == 'bank' or self.journal_id.type == 'cash':
                self.hide_check_payment = False
            else:
                self.hide_check_payment = True
        res['domain']['payment_type'] = self.payment_type
        return res

    @api.multi
    @api.depends('journal_id')
    def _compute_hide_check_payment(self):
        for payment in self:
            if payment.payment_type == 'transfer':
                payment.hide_check_payment = True
                continue
            if not payment.journal_id:
                payment.hide_check_payment = True
                continue
            if payment.payment_type == 'outbound' or payment.payment_type == 'inbound':
                if payment.journal_id.type == 'bank' or payment.journal_id.type == 'cash':
                    payment.hide_check_payment = False
                else:
                    payment.hide_check_payment = True
