from django_components import component

@component.register("header")
class Header(component.Component):
    template_name = "header/template.html"


    class Media:
        css = "header/style.css"
        
        
@component.register("sidebar")
class sidebar(component.Component):
    template_name = "sidebar.html"
    
@component.register("user-avatar")
class UserAvatar(component.Component):
    template_name = "user-avatar.html"
    

@component.register("select-gudang")
class SelectGudang(component.Component):
    template_name = "select-gudang.html"
    
    class Media:
        js = "select-gudang.js"