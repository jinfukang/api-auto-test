import time

import pytest


if __name__ == '__main__':
    times = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    pytest.main([
        "--html=./reports/reports_%s.html" % times,
        "--self-contained-html"
    ])