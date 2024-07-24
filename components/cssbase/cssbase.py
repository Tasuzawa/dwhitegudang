from django_components import component

@component.register("cssbase")
class Cssbase(component.Component):
    template_name = "cssbase/template.html"


    class Media:
        css = "cssbase/style.css"