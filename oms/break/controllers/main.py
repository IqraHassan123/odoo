from odoo import http
import werkzeug
from odoo.http import request

class CustomAuthSignUpHome(http.Controller):
    @http.route("web/signup", type="http", auth="public",sitemap=True, website=True)
    def web_auth_signup(self,**kw):
        qcontext=self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                values={
                    'login':qcontext.get('login'),
                    'password':qcontext.get('password'),
                    'name':qcontext.get('name'),
                    'phone_number':kw.get('phone_number'),
                    'mobile':kw.get('mobile'),
                }
                self.do_signup(qcontext,values)
                return request.redirect('web/login')
            except Exception as e:
             qcontext['error'] = str(e)

        response = request.render('auth_signup.signup', qcontext)
        return response


    def do_signup(self, qcontext, values):
        """ Custom signup process to include custom fields """
        user = request.env['res.users'].sudo().create(values)
        request.env.cr.commit()
        credential = {'login': user.login, 'password': values['password'], 'type': 'password'}
        request.session.authenticate(request.db, credential)
