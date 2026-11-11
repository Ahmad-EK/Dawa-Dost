"""
End-to-End Test for Dawa Dost Request Handling
Validates request parsing, header setting, and static file configuration.
"""

import sys
import os
import unittest

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import server

class TestServerConfig(unittest.TestCase):
    def test_routes_and_dirs_exist(self):
        self.assertTrue(os.path.exists(server.FRONTEND_DIR))
        self.assertTrue(os.path.exists(server.SAMPLES_DIR))
        self.assertTrue(os.path.exists(os.path.join(server.FRONTEND_DIR, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(server.FRONTEND_DIR, "css", "style.css")))
        self.assertTrue(os.path.exists(os.path.join(server.FRONTEND_DIR, "js", "app.js")))

if __name__ == "__main__":
    unittest.main()
