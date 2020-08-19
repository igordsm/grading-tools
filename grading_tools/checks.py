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
            tokens_expected = test.output.strip().split()
            tokens_test = stdout.strip().split()
            return tokens_expected == tokens_test
        else:
            return test.stderr.strip() == stderr.strip()
