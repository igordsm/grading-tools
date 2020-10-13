from collections import defaultdict, namedtuple
import argparse
import filecmp
import re
import os
import subprocess
import psutil
import inspect

from .config import TestConfiguration

class ProgramTest:
    def __init__(self, cmd, tests={}):
        self.program_cmd = cmd
        self.tests = tests

    def run_program(self, test):
        env = os.environ.copy()
        env.update(test.environ)
        proc = subprocess.run([self.program_cmd], input=test.input.encode('ascii'),
                          capture_output=True, env=env, timeout=test.time_limit)
        out_proc = str(proc.stdout, 'ascii').strip()
        err_proc = str(proc.stderr, 'ascii').strip()
        return out_proc, err_proc

    def main(self):
        pass_all = True
        for arq, test in self.tests.items():
            print(f'====================\nEntrada: {arq}')
            before_running_predicate = lambda arg: inspect.ismethod(arg) and \
                                                    arg.__name__.startswith('before_')
            methods_before = inspect.getmembers(self, predicate=before_running_predicate)

            after_running_predicate = lambda arg: inspect.ismethod(arg) and \
                                                    arg.__name__.startswith('after_')
            methods_after = inspect.getmembers(self, predicate=after_running_predicate)

            try:
                for method in methods_before:
                    method()

                stdout, stderr = self.run_program(test)
                
                for method in methods_after:
                    method()
            except subprocess.TimeoutExpired:
                self.timeout(test)
                pass_all = False
            else:
                get_all_tests_predicate = lambda arg: inspect.ismethod(arg) and \
                                                    arg.__name__.startswith('test_')
                for name, method in inspect.getmembers(self, predicate=get_all_tests_predicate):
                    name = name[5:].replace('_', ' ').title()
                    test_result = method(test, stdout, stderr)
                    print(name, test_result)
                    pass_all = test_result and pass_all

        #print('====================\nValidated:', pass_all)
        return pass_all
        
    def timeout(self, test):
        print(f'Timeout exceeded: {test.time_limit}s')



class RepeaterTest(ProgramTest):
    def test_same_result_as_last_execution(self, test, stdout, stderr):
        try:
            getattr(self, 'last_test')
        except AttributeError:
            self.last_test = (stdout, stderr)
            return True

        equal = stdout == self.last_test[0] and stderr == self.last_test[1]
        self.last_test = (stdout, stderr)
        return equal

    def __init__(self, program_cmd, test, num_repetitions):
        tests = {f'Execution {i}': test for i in range(num_repetitions)}
        super().__init__(program_cmd, tests)

