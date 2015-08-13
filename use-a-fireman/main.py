from webapp2 import WSGIApplication
from Server import MainRequestHandler
from Server import SomeRequestHandler
from Server import OtherRequestHandler

app = WSGIApplication([
    ('/'              ,MainRequestHandler),
    ('/email'           ,SomeRequestHandler),
])