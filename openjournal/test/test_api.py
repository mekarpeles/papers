import unittest
import requests

from api.v1.paper import Paper

class TestAPI(unittest.TestCase):
    def test_papers(self):
        """Should create a paper if none exist and then verify the
        len(Paper.getall())"""
        pass
