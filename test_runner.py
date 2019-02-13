import unittest

if __name__ == "__main__":
    test_loader = unittest.defaultTestLoader.discover(".")
    runner = unittest.TextTestRunner()
    runner.run(test_loader)
