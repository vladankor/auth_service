#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser

from django import setup as django_setup
from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Return the number of tests that failed.
        """
        self.setup_test_environment()
        # Изменен порядок вызовов: сначала инициализируем БД,
        # потом инициализируем тесты, т.к. иначе фикстуры не прогрузятся из-за
        # несуществующей БД
        old_config = self.setup_databases()
        suite = self.build_suite(test_labels, extra_tests)
        self.run_checks()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django_setup()

    parser = ArgumentParser()
    TestRunner.add_arguments(parser)
    args = parser.parse_args(sys.argv[1:])


    test_runner = TestRunner(
        pattern=getattr(args, 'pattern', None),
        top_level=getattr(args, 'top_level', None),
        verbosity=getattr(args, 'verbosity', 1),
        interactive=getattr(args, 'interactive', True),
        failfast=getattr(args, 'failfast', False),
        keepdb=getattr(args, 'keepdb', False),
        reverse=getattr(args, 'reverse', False),
        debug_mode=getattr(args, 'debug_mode', False),
        debug_sql=getattr(args, 'debug_sql', False),
        parallel=getattr(args, 'parallel', 0),
        tags=getattr(args, 'tags', None),
        exclude_tags=getattr(args, 'exclude_tags', None)
    )

    failures = test_runner.run_tests(['tests'])

    sys.exit(bool(failures))