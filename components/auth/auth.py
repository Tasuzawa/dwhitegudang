from django_components import component

@component.register('register')
class register(component.Component):
    template_name = "register.html"

    def get_context_data(self, action, link):
        context = {
            'action': action,
            'link': link,
        }
        return context
        
    class Media:
        css = "register.css"
#        js = "login.js"

@component.register('login')
class Login(component.Component):
    template_name = "login.html"

    def get_context_data(self, action, link):
        context = {
            'action': action,
            'link': link,
        }
        return context
        
    class Media:
        css = "login.css"
#        js = "login.js"



#@component.register("auth")
#class Auth(component.Component):
#    template_name = "auth/template.html"

#    def get_context_data(self, value):
#        return {
#            "param": "sample value",
#        }

#    class Media:
#        css = "auth/style.css"
#        js = "auth/script.js"