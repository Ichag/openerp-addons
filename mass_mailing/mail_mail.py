# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.osv import osv, fields


class MailMail(osv.Model):
    """Add the mass mailing campaign data to mail"""
    _name = 'mail.mail'
    _inherit = ['mail.mail']

    _columns = {
        'mass_mailing_segment_id': fields.many2one(
            'mail.mass_mailing.segment', 'Mass Mailing Segment',
            ondelete='set null',
        ),
        'mass_mailing_campaign_id': fields.related(
            'mass_mailing_segment_id', 'mass_mailing_campaign_id',
            type='many2one', ondelete='set null',
            relation='mail.mass_mailing.campaign',
            store=True, readonly=True,
        ),
    }
