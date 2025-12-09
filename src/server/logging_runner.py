from django.test.runner import DiscoverRunner
import unittest
import os
import json
from datetime import datetime

"""python manage.py test tests.modul.test_modul_quiz"""

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
        group = "general"
        submodule = "general"

        if test_labels:
            parts = test_labels[0].split('.')

            # Extract test group (modul, integration, ...)
            if len(parts) > 1:
                group = parts[1]

            # Extract the test module name from the file name
            filename = parts[-1]  # e.g. "test_modul_quiz"
            name_parts = filename.split('_')

            # last part is usually the test module name
            if len(name_parts) >= 2:
                submodule = name_parts[-1]  # quiz / accounts / account

        short_name = f"{group}_{submodule}"

        # Run Django tests
        suite = self.build_suite(test_labels, **kwargs)
        runner = unittest.TextTestRunner(resultclass=LoggingTestResult, verbosity=2)
        result = runner.run(suite)

        # Save logs
        folder = os.path.join(os.path.dirname(__file__), "test_logs")
        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(
            folder,
            f"test_results_{short_name}_{datetime.now().strftime('%m-%d')}.txt"
        )

        with open(filename, "w") as f:
            json.dump(result.logged_results, f, indent=2)

        print(f"Test results saved to {filename}")

        return len(result.failures) + len(result.errors)
