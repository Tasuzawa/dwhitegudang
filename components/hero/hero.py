from django_components import component

#@component.register("hero")
#class Hero(component.Component):
#    template_name = "hero/template.html"

#    class Media:
#        css = "hero/style.css"
        
        
        
@component.register("hero-wellcome")
class Hero_welcome(component.Component):
    template_name = "hero-wellcome.html"

    class Media:
        css = "hero-wellcome.css"