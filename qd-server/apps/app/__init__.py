
from turbo import register

import app


register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/qiandao', app.QiandaoHandler),
])
register.register_group_urls('/god', [
    ('', app.AdminHandler),
])
