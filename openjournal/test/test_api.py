import unittest
import requests

from api.v1.paper import Paper

class TestAPI(unittest.TestCase):
    def test_papers(self):
        papers = Paper.getall()
        self.assertTrue(len(papers))
