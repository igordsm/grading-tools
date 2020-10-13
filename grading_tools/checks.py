class CheckOutputMixin:
    def test_program_output(self, test, stdout, stderr):
        if test.ignore_whitespace:
            output_tokens = test.output.strip().split()
            stdout_tokens = stdout.strip().split()
            return output_tokens == stdout_tokens
        else:
            return test.output.strip() == stdout.strip()


class CheckStderrMixin:
    def test_program_stderr(self, test, stdout, stderr):
        if test.ignore_whitespace:
            tokens_expected = test.stderr.strip().split()
            tokens_test = stderr.strip().split()
            return tokens_expected == tokens_test
        else:
            return test.stderr.strip() == stderr.strip()


class CheckMultiCorePerformance:
    def before_run(self, test):
        psutil.cpu_percent(percpu=True)

    def after_run(self, test, stdout, stderr):
        self.cpu_percent = psutil.cpu_percent(percpu=True)
    
    def test_multi_core_performance(self, test, stdout, stderr):
        total_cpu = len(self.cpu_percent)
        multi_core_performance = (sum(self.cpu_percent) / total_cpu) > 50
        return multi_core_performance


