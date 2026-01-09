import sphinx
from docutils.parsers.rst import directives
from docutils import nodes


class OnlyCustomized(sphinx.directives.other.Only):

    def run(self, *args):
        env = self.state.document.settings.env
        env.app.builder.tags.add('TRUE')
        #print(repr(self.arguments[0]))
        if env.app.builder.tags.eval_condition(self.arguments[0]):
            node_list = super(OnlyCustomized, self).run()
            if len(node_list) == 1:
                node_list[0]['expr'] = 'TRUE'
        else:
            # parse content as comment
            node = nodes.comment()
            node.document = self.state.document
            self.set_source_info(node)
            node['expr'] = self.arguments[0]
            self.state.nested_parse(self.content, self.content_offset, node, match_titles=True)
            node.children = []
            node_list = [node]
        
        return node_list


def setup(app):
    directives.register_directive('only', OnlyCustomized)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '1.0.2'}