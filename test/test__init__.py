import unittest
from scikit_rest_wrapper import App

class AppTest(unittest.TestCase):
    def test_creates_only_one_app_instance(self):
        """The monostate pattern should only create a single instance."""
        app1 = App().get_app()
        app2 = App().get_app()

        self.assertTrue(app1 == app2)

    def test_creates_only_one_json_instance(self):
        """The monostate pattern should only create a single instance."""
        json1 = App().get_json()
        json2 = App().get_json()

        self.assertTrue(json1 == json2)


