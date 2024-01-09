from subprocess import run, CompletedProcess

from pytest_cookies.plugin import Result


def test_run_black(
    hot_cookie: Result, virtual_environment_context: dict
) -> None:
    completed_process: CompletedProcess = run(
        ["black", "."],
        cwd=hot_cookie.project_path,
        env=virtual_environment_context,
    )
    assert completed_process.returncode == 0


def test_run_tests(
    hot_cookie: Result, virtual_environment_context: dict
) -> None:
    completed_process: CompletedProcess = run(
        ["pytest"], cwd=hot_cookie.project_path, env=virtual_environment_context
    )
    assert completed_process.returncode == 0
