import os
import glob
from subprocess import Popen
from os.path import join, dirname, realpath, basename
def run_all():
    d = dirname(realpath(__file__))
    env = dict(os.environ)
    env['PYTHONPATH'] = dirname(d)
    env['NOGRAPHICS'] = '1'
    failed = []
    for filename in glob.glob(join(d, 'Demo*.py')):
        proc = Popen(['python', filename, '-v', '0'], env=env)
        proc.wait()
        if proc.returncode != 0:
            failed.append(filename)
    assert not failed

if __name__ == '__main__':
    run_all()
