import unittest
from paste.fixture import TestApp
from nose.tools import *
from main import app

class TestRoutes(unittest.TestCase):
    def test_index(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        r = testApp.get('/')
        assert_equal(r.status, 200)
        r.mustcontain('openjournal')
    
    
