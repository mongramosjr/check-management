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

from openerp import models, fields, api, _
from openerp.exceptions import UserError, ValidationError

class CheckPaymentTransaction(models.Model):
    
    _name = 'check.payment.transaction.payment'
    _description = 'Check Payment'
    _inherits = {'check.payment.transaction': 'check_payment_transaction_id'}


    check_payment_transaction_id = fields.Many2one('check.payment.transaction', required=True, string='Payment Reference', ondelete='cascade')
    account_payment_id = fields.Many2one('account.payment', readonly=True, string='Payment Reference', ondelete='cascade', index=True, states={'draft': [('readonly', False)]})

    @api.multi
    def _compute_payment_type(self):
        for rec in self:
            if rec.account_payment_id:
                rec.payment_type = rec.account_payment_id.payment_type
            else:
                rec.payment_type = 'inbound'
