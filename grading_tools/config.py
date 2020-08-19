from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import Optional, Dict

import glob
import os.path as osp

def get_file_contents(fname):
    if not fname:
        return ''

    try:
        with open(fname) as f:
            return f.read()
    except IOError:
        return ''


@dataclass
class TestConfiguration:
    input: str = ''
    output: str = ''
    stderr: str = ''
    check_stderr: bool = True
    time_limit: Optional[int] = None
    ignore_whitespace: bool = True
    environ: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_file(input_path, output_path, stderr_path=None, **kwargs):
        input_txt = get_file_contents(input_path)
        output_txt = get_file_contents(output_path)
        stderr = ''
        if stderr_path:
            stderr = get_file_contents(stderr_path)

        return TestConfiguration(input_txt, output_txt, stderr, **kwargs)

    @staticmethod
    def from_pattern(dir, in_pattern, out_pattern, err_pattern=None, **kwargs):
        tests = {}

        input_files = sorted(glob.glob(osp.join(dir, in_pattern)))
        output_files = sorted(glob.glob(osp.join(dir, out_pattern)))
        err_files = [None] * len(input_files)

        if err_pattern is not None:
            err_files = sorted(glob.glob(osp.join(dir, err_pattern)))

        for (inp, out, err) in zip(input_files, output_files, err_files):
            tests[inp] = TestConfiguration(
                                get_file_contents(inp), 
                                get_file_contents(out), 
                                get_file_contents(err), 
                                **kwargs)

        return tests
