from django_components import component

@component.register("public")
class Public(component.Component):
    template_name = "public/template.html"

@component.register("favicon")
class favicon(component.Component):
    template_name = "favicon.html"