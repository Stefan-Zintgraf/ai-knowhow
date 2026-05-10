from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
#from sphinx.domains.cpp import nodes

class emIoControl(SphinxDirective):
    _default_ioControl_Parms = { 
        'pbyInBuf' : ['[in]', 'Should be set to EC_NULL'],
        'dwInBufSize' : ['[in]', 'Should be set to 0'],
        'pbyOutBuf' : ['[out]', 'Should be set to EC_NULL'],
        'dwOutBufSize' : ['[in]', 'Should be set to 0'],
        'pdwNumOutData' : ['[out]', 'Should be set to EC_NULL']
    }
    has_content = True
    required_arguments = 1
    option_spec = {
        'pbyinbuf' : directives.unchanged_required,
        'dwinbufsize' : directives.unchanged_required,
        'pbyoutbuf' : directives.unchanged_required, 
        'dwoutbufsize' : directives.unchanged_required,
        'pdwnumoutdata' : directives.unchanged_required,
    }
    
    def run(self):
        
        dl_cppfunc = nodes.definition_list(classes=['cpp function']) #TODO cpp function simple
        dl_cppfunc_item = nodes.definition_list_item()
        dt_cppfunc = nodes.term()
        dt_cppfunc += nodes.strong(text=(self.name + ' - ' + self.arguments[0]))
        dl_cppfunc_item += dt_cppfunc
        dl_cppfunc += dl_cppfunc_item
        dd_cppfunc = nodes.definition()
        
        dl = nodes.definition_list()
        # heading parameter
        dl_item = nodes.definition_list_item()
        dt = nodes.term()
        dt += nodes.strong(text='Parameter')
        dl_item += dt
        dl += dl_item
        
        # parameter list
        dd = nodes.definition()
        dd_l = nodes.bullet_list()
        # list items
        for parm in self._default_ioControl_Parms:
            dd_l_item = nodes.list_item()
            dd_l_item_p = nodes.paragraph()
            dd_l_item_p += nodes.literal(text=parm)
            parm_dir = self._default_ioControl_Parms[parm][0]
            parm_desc = self._default_ioControl_Parms[parm][1]
            if parm.lower() in self.options:
                parm_desc = self.options[parm.lower()]
            dd_l_item_p += nodes.Text(': ' + parm_dir + ' ' + parm_desc)          
            dd_l_item += dd_l_item_p
            dd_l += dd_l_item
        
        dd += dd_l       
        dl += dd
        dd_cppfunc += dl
        
        if self.name.lower() == 'emiocontrol':
            # return
            dl = nodes.definition_list()
            dl_item = nodes.definition_list_item()
            dt = nodes.term()
            dt += nodes.strong(text='Return')
            dd_l = nodes.bullet_list()
            dl_item += dt
            dl += dl_item
            dd = nodes.definition()
            dd_p = nodes.paragraph()
            dd_p += nodes.Text('EC_E_NOERROR or error code')
            dd += dd_p
            dl += dd
            dd_cppfunc += dl
        
        dl_cppfunc += dd_cppfunc
        
        return [dl_cppfunc]
        #return [dl]

def setup(app):
    app.add_directive('emiocontrol', emIoControl)
    app.add_directive('emnotify', emIoControl)
    app.add_directive('emrasnotify', emIoControl)

    app.add_directive('emoniocontrol', emIoControl)
    app.add_directive('emonnotify', emIoControl)
    app.add_directive('emonrasnotify', emIoControl)

    app.add_directive('esiocontrol', emIoControl)
    app.add_directive('esnotify', emIoControl)
    app.add_directive('esrasnotify', emIoControl)

    app.add_directive('rasnotifycallback', emIoControl)
    
    #logger = logging.getLogger(__name__)
    #logger.info('Hello, this is an extension!', color='blue')
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }