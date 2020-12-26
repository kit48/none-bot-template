import os
import sys
import subprocess

target_dir = r'D:\Program Files\go-cqhttp'
qq = 'go-cqhttp-v0.9.35-fix1-windows-amd64.exe'


def run_qq():
    os.chdir(target_dir)
    # usage: https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
    process = subprocess.Popen([qq], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline().decode(sys.stdout.encoding)
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


if __name__ == '__main__':
    run_qq()
