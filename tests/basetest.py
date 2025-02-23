"""
Created on 2021-08-19

@author: wf
"""

import getpass
import os
import threading
import time
import unittest
from functools import wraps


class Profiler:
    """
    simple profiler
    """

    def __init__(self, msg, profile=True, with_start: bool = True):
        """
        construct me with the given msg and profile active flag

        Args:
            msg(str): the message to show if profiling is active
            profile(bool): True if messages should be shown
        """
        self.msg = msg
        self.profile = profile
        if with_start:
            self.start()

    def start(self):
        """
        start profiling
        """
        self.starttime = time.time()
        if self.profile:
            print(f"Starting {self.msg} ...")

    def time(self, extraMsg=""):
        """
        time the action and print if profile is active
        """
        elapsed = time.time() - self.starttime
        if self.profile:
            print(f"{self.msg}{extraMsg} took {elapsed:5.1f} s")
        return elapsed


class Basetest(unittest.TestCase):
    """
    base test case
    """

    def setUp(self, debug=False, profile=True):
        """
        setUp test environment
        """
        unittest.TestCase.setUp(self)
        self.debug = debug
        self.profile = profile
        msg = f"test {self._testMethodName}, debug={self.debug}"
        self.profiler = Profiler(msg, profile=self.profile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.profiler.time()

    @staticmethod
    def inPublicCI():
        """
        are we running in a public Continuous Integration Environment?
        """
        publicCI = getpass.getuser() in ["travis", "runner"]
        jenkins = "JENKINS_HOME" in os.environ
        return publicCI or jenkins

    @staticmethod
    def isUser(name: str):
        """Checks if the system has the given name"""
        return getpass.getuser() == name

    @staticmethod
    def timeout(seconds):
        """
        Decorator to enforce a timeout on test methods.

        params:
          1: seconds: Timeout in seconds
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = [None]
                exception = [None]

                def target():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        exception[0] = e

                thread = threading.Thread(target=target)
                thread.start()
                thread.join(seconds)

                if thread.is_alive():
                    raise TimeoutError(f"Test timed out after {seconds} seconds")

                if exception[0] is not None:
                    raise exception[0]

                return result[0]

            return wrapper

        return decorator


if __name__ == "__main__":
    unittest.main()
