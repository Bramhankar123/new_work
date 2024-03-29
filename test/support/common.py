import os
import subprocess

test_dir = str(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.join(test_dir, '..', '..')


def decode_utf8(bytes):
    return bytes.decode('utf-8')


def run_command(exe, args, env=None):
    cwd = project_root
    if env is None:
        result = subprocess.run([exe] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, cwd=cwd)
    else:
        result = subprocess.run(str.join (' ', [exe] + args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd, env=env)
    result.stdout = decode_utf8(result.stdout)
    result.stderr = decode_utf8(result.stderr)
    return result


def run_shell(command):
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def get_dojo_exe():
    dojo_exe = os.path.join(test_dir, '..', '..', 'bin', 'dojo')
    dojo_exe_absolute_path = os.path.abspath(dojo_exe)
    return dojo_exe_absolute_path


def run_dojo(args, env=None):
    dojo_exe = get_dojo_exe()
    return run_command(dojo_exe, args, env)


def run_dojo_and_set_bash_func(args, env=None):
    dojo_exe = os.path.join(test_dir, '..', '..', 'bin', 'dojo')
    fullArgs = 'source ' + test_dir + '/../test-files/test-bash-function.sh && ' + dojo_exe + ' ' + ' '.join(args)
    proc = subprocess.Popen(['bash','-c',fullArgs], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def assert_no_warnings_or_errors(text, full_output_to_print):
    assert not 'warn' in text.lower(), full_output_to_print
    assert not 'error' in text.lower(), full_output_to_print
