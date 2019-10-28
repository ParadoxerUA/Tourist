import unittest


class BasicTest(unittest.TestCase):
    """Basic test class"""
    
    @classmethod
    def setUpClass(cls):
        """Instructions that will be executed before every single test"""
        import sys
        if not "./api" in sys.path:
            sys.path.append("./api")
        from app import create_app
        from config import DebugConfig
        cls.app = create_app(DebugConfig)
        cls.test_client = cls.app.test_client()
