from django_components import component

@component.register("header")
class Header(component.Component):
    template_name = "header/template.html"


    class Media:
        css = "header/style.css"