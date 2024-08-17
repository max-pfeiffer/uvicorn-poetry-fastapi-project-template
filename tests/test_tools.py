"""Test utilities."""

from subprocess import CompletedProcess, run

from pytest_cookies.plugin import Result


def test_run_ruff(hot_cookie: Result, virtual_environment_context: dict) -> None:
    """Test running ruff in generated project.

    :param hot_cookie:
    :param virtual_environment_context:
    :return:
    """
    completed_check_process: CompletedProcess = run(
        ["ruff", "check", "--exit-zero", "--config", "pyproject.toml"],
        cwd=hot_cookie.project_path,
        env=virtual_environment_context,
    )
    assert completed_check_process.returncode == 0

    completed_format_process: CompletedProcess = run(
        ["ruff", "format", "--config", "pyproject.toml"],
        cwd=hot_cookie.project_path,
        env=virtual_environment_context,
    )
    assert completed_format_process.returncode == 0


def test_run_pre_commit_handler(
    hot_cookie: Result, virtual_environment_context: dict
) -> None:
    """Test running pre-commit handler in generated project.

    :param hot_cookie:
    :param virtual_environment_context:
    :return:
    """
    completed_check_process: CompletedProcess = run(
        ["git", "init"],
        cwd=hot_cookie.project_path,
        env=virtual_environment_context,
    )
    assert completed_check_process.returncode == 0

    completed_check_process: CompletedProcess = run(
        ["pre-commit", "run", "-a"],
        cwd=hot_cookie.project_path,
        env=virtual_environment_context,
    )
    assert completed_check_process.returncode == 0


def test_run_tests(hot_cookie: Result, virtual_environment_context: dict) -> None:
    """Test running tests in generated project.

    :param hot_cookie:
    :param virtual_environment_context:
    :return:
    """
    completed_process: CompletedProcess = run(
        ["pytest"], cwd=hot_cookie.project_path, env=virtual_environment_context
    )
    assert completed_process.returncode == 0
