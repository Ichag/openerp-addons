# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.tools.translate import _


class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def get_interested_action(self, cr, uid, interested, context=None):
        try:
            model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'crm_partner_assign', 'crm_lead_channel_interested_act')
        except ValueError:
            raise osv.except_osv(_('Error!'), _("The CRM Channel Interested Action is missing"))
        action = self.pool[model].read(cr, uid, action_id, context=context)
        action_context = eval(action['context'])
        action_context['interested'] = interested
        action['context'] = str(action_context)
        return action

    def case_interested(self, cr, uid, ids, context=None):
        return self.get_interested_action(cr, uid, True, context=context)

    def case_disinterested(self, cr, uid, ids, context=None):
        return self.get_interested_action(cr, uid, False, context=context)
