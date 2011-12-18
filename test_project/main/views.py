from django.views.generic import TemplateView

class DemoView(TemplateView):
    template_name = 'panels/treemap_test.html'

    def get_context_data(self):
        data = '''
            ["Test",null,0,0],
            ["US","Test",10,1],
            ["UK","Test",20,5]
                '''
        return {'data_demo': data}
