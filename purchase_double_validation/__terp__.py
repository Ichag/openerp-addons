#!/usr/bin/python
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "purchase_double_validation",
    "version" : "1.1",
    "category": "Generic Modules/ Purchases Double Validation ",
    "depends" : ["base","purchase"],
    "author" : "Tiny",
    "description": """
		Subject,Date,Status		
    """,
    'author': 'Tiny',
    'website': 'http://www.openerp.com',

    'init_xml': [],
    'update_xml': [
                   'purchase_double_validation_view.xml',
                   'purchase_double_validation_workflow.xml',
                   'wizard/purchase_double_validation_wizard_view.xml', ],
    'demo_xml': [],
    'installable': True,
    'active': False,

}
