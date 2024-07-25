from django_components import component

@component.register("jsbase")
class Jsbase(component.Component):
    template_name = "jsbase/template.html"



    class Media:

        js = "jsbase/script.js"