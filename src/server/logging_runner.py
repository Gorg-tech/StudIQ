from django.test.runner import DiscoverRunner
import unittest
import os
import json
from datetime import datetime

class LoggingTestResult(unittest.TextTestResult):
    """Tracks all test outcomes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.logged_results.append({
            "test": str(test),
            "status": "SUCCESS",
            "time": str(datetime.now())
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.logged_results.append({
            "test": str(test),
            "status": "FAILURE",
            "error": self._exc_info_to_string(err, test),
            "time": str(datetime.now())
        })

    def addError(self, test, err):
        super().addError(test, err)
        self.logged_results.append({
            "test": str(test),
            "status": "ERROR",
            "error": self._exc_info_to_string(err, test),
            "time": str(datetime.now())
        })

class LoggingTestRunner(DiscoverRunner):
    MODULE_NAME_MAP = {
        "test_moduls": "quiz",
        "test_accounts": "acc",
    }

    def run_tests(self, test_labels, **kwargs):
        # Determine short name based on first label
        if test_labels:
            first_label = test_labels[0].split('.')[-1]
            short_name = self.MODULE_NAME_MAP.get(first_label, "general")
        else:
            short_name = "general"

        # Run Django tests normally, but wrap the result
        suite = self.build_suite(test_labels, **kwargs)
        runner = unittest.TextTestRunner(resultclass=LoggingTestResult, verbosity=2)
        result = runner.run(suite)

        # Save results to file
        folder = os.path.join(os.path.dirname(__file__), "test_logs")
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(
            folder,
            f"test_results_{short_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
        )
        with open(filename, "w") as f:
            json.dump(result.logged_results, f, indent=2)

        print(f"Test results saved to {filename}")

        # Return total failures + errors as Django expects
        return len(result.failures) + len(result.errors)