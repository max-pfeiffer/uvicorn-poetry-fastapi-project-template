from subprocess import run, CompletedProcess

from tests.utils import setup_virtual_environment


def test_run_black(hot_cookie) -> None:
    environment_variables = setup_virtual_environment(hot_cookie)

    completed_process: CompletedProcess = run(
        ["black", "."], cwd=hot_cookie.project_path, env=environment_variables
    )
    assert completed_process.returncode == 0


def test_run_tests(hot_cookie) -> None:
    environment_variables = setup_virtual_environment(hot_cookie)

    completed_process: CompletedProcess = run(
        ["pytest"], cwd=hot_cookie.project_path, env=environment_variables
    )
    assert completed_process.returncode == 0
