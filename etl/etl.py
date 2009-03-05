
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2404-2409 Tiny SPRL (<http://tiny.be>). All Rights Reserved
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


from osv import osv, fields


class etl_project(osv.osv):
    _name='etl.project'
    _columns={
              'name' : fields.char('Name', size =64), 
              'job_ids' : fields.one2many('etl.job', 'project_id', 'Jobs')
    }
etl_project()

class etl_channel(osv.osv):
    _name='etl.channel'
    _columns={
              'name' : fields.char('Channel Name', size=64, required=True), 
              'code' : fields.char('Code', size=24, required=True), 
              'type' : fields.selection([('logger', 'Logger'), ('transition', 'Transition')], 'Type'), 
              }
etl_channel()

class etl_transformer(osv.osv):
    _name='etl.transformer'
        
    _columns={
              'name' : fields.char('Name', size=64, required=True), 
              'tranformer_line_ids' : fields.one2many('etl.transformer.line', 'tranformer_id', 'ETL Transformer'), 
              }
    
etl_transformer()


class etl_transformer_line(osv.osv):
    _name='etl.transformer.line'
        
    _columns={
              'name' : fields.char('Name', size=64, required=True), 
              'tranformer_id' : fields.many2one('etl.transformer', 'ETL Transformer'), 
              'type' : fields.selection([('integer', 'INTEGER'), ('string', 'STRING'), ('date', 'DATE'), ('datetime', 'DATETIME'), ('time', 'TIME'), ('float', 'FLOAT'), ('long', 'LONG'), ('complex', 'COMPLEX'), ('boolean', 'BOOLEAN')], 'Type'), 
              }
    
etl_transformer_line()

class etl_connector_type(osv.osv):
    _name='etl.connector.type'
    
    _columns={
              'name' : fields.char('Name', size=64, required=True), 
              'code' : fields.char('Code', size=24, required=True), 
              }
etl_connector_type()


class etl_connector(osv.osv):
    _name='etl.connector'
    
    def _get_connector_type(self, cr, uid, context={}):
            c_obj = self.pool.get('etl.connector.type')
            type_ids = c_obj.search(cr, uid, [])
            result = c_obj.read(cr, uid, type_ids, ['code', 'name'], context)
            return [(r['code'], r['name']) for r in result]
        
    _columns={
              'name' : fields.char('Connector Name', size=64, required=True), 
              'type' : fields.selection(_get_connector_type, 'Connector Type'), 
              'uri' : fields.char('URL Path', size=64), 
              'db' : fields.char('Database', size=64), 
              'login' : fields.char('Login Name', size=64), 
              'passwd' : fields.char('Password', size=64), 
              'obj' : fields.char('Object', size=64), 
              'con_type' : fields.char('Connection Type', size=64), 
              'bufsize' : fields.integer('Buffer Size')
              }
    
    _defaults = {
                'obj' : lambda *a : '/xmlrpc/object', 
                'con_type' :  lambda *a : 'xmlrpc'
                }
    
etl_connector()


class etl_job(osv.osv):
    _name= 'etl.job'
    _columns={
              'name' : fields.char('Name', size=24, required=True), 
              'project_id' : fields.many2one('etl.project', 'ETL Project', readonly=True), 
              'user_id' : fields.many2one('res.users', 'Responsible', size=64), 
              'author' : fields.char('Author', size =50), 
              'is_start' : fields.boolean('Starting Job'), 
              'notes' : fields.text('Notes'), 
              'component_ids' : fields.many2many('etl.component', 'rel_job_comp', 'c_id', 'j_id', 'Components'), 
              'state' : fields.selection([('open', 'Open'), ('start', 'Started'), ('pause', 'Pause'), ('stop', 'Stop'), ('close', 'Close')], 'State', readonly=True), 
              'running_process' : fields.char('Running Processes', size=24), 
              'total_process' : fields.char('Total Processes', size=24)
              }
    
    _defaults = {
                'state': lambda *a: 'open', 
                }    
etl_job()


class etl_component_type(osv.osv):
    _name='etl.component.type'
    
    _columns={
              'name' : fields.char('Name', size=64, required=True), 
              'code' : fields.char('Code', size=24, required=True), 
              'parent_component' : fields.many2one('etl.component.type', 'Parent Component'), 
              }
etl_component_type()


class etl_component(osv.osv):
        _name='etl.component'
        
#        def _get_component_type(self, cr, uid, context={}):
#            c_obj = self.pool.get('etl.component.type')
#            type_ids = c_obj.search(cr, uid, [])
#            result = c_obj.read(cr, uid, type_ids, ['code', 'name'], context)
#            return [(r['code'], r['name']) for r in result]
        
        _columns={
                'name' : fields.char('Name', size=30, required=True), 
                'type' : fields.many2one('etl.component.type', 'Component Type'), 
                'job_id' : fields.many2one('etl.job', 'Job', required=True), 
                'trans_in_ids' : fields.one2many('etl.transition', 'source_component_id', 'Source ID'), 
                'trans_out_ids' : fields.one2many('etl.transition', 'destination_component_id', 'Destination ID')
                  }
etl_component()

class etl_transition(osv.osv):
        _name = 'etl.transition'
        _description = "This defines  ETL job's transition"
        
        def _get_channels(self, cr, uid, context={}):
            c_obj = self.pool.get('etl.channel')
            ch_ids = c_obj.search(cr, uid, [('type', '=', 'transition')])
            result = c_obj.read(cr, uid, ch_ids, ['code', 'name'], context)
            return [(r['code'], r['name']) for r in result]
        
        _columns = {
                  'name' : fields.char('Name', size=30, required=True), 
                  'type' : fields.selection([('data', 'Data Transition'), ('trigger', 'Trigger Transition')], 'Transition Type', required=True), 
                  'source_component_id' : fields.many2one('etl.component', 'Source Component', required=True), 
                  'destination_component_id' : fields.many2one('etl.component', 'Destination Component', required=True), 
                  'channel_source' : fields.selection(_get_channels, 'Source Channel'), 
                  'channel_destination' : fields.selection(_get_channels, 'Destination Channel'), 
                  'state' : fields.selection([('open', 'Open'), ('start', 'Start'), ('pause', 'Pause'), ('stop', 'Stop'), ('close', 'Close')], 'State', readonly=True), 
                  }
        
        _defaults = {
                'state': lambda *a: 'open', 
                }
etl_transition()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
