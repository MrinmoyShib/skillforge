"""
Development & testing fallback execution engine.
Emulates compilation checks and output comparison when Judge0 is not running.
"""
import time
import re
import sys
import subprocess
from .base import AbstractExecutionEngine, ExecutionResult
from ..models import SubmissionStatus


class DevFallbackEngine(AbstractExecutionEngine):
    """
    Safe fallback engine for local dev and pytest when Judge0 stack is offline.
    Executes Python directly via subprocess and compares outputs accurately.
    """

    def is_available(self) -> bool:
        return True

    def execute(
        self,
        *,
        source_code: str,
        language: str,
        stdin: str,
        expected_output: str,
        time_limit: float = 2.0,
        memory_limit: int = 262144
    ) -> ExecutionResult:
        # Check basic non-empty source
        if not source_code or not source_code.strip():
            return ExecutionResult(
                status=SubmissionStatus.COMPILATION_ERROR,
                execution_time=0.01,
                memory_usage=1240,
                compile_output="error: source code cannot be empty."
            )

        # 1. Fast mock checks for unit testing
        if "syntax_error" in source_code:
            return ExecutionResult(
                status=SubmissionStatus.COMPILATION_ERROR,
                execution_time=0.01,
                memory_usage=1240,
                compile_output="error: syntax error before token"
            )

        if "force_wrong_answer" in source_code:
            return ExecutionResult(
                status=SubmissionStatus.WRONG_ANSWER,
                execution_time=0.02,
                memory_usage=4500,
                stdout="wrong output\n"
            )

        if "raise_runtime_error" in source_code:
            return ExecutionResult(
                status=SubmissionStatus.RUNTIME_ERROR,
                execution_time=0.02,
                memory_usage=3200,
                stderr="Runtime error: execution terminated abnormally."
            )

        condensed = source_code.replace(" ", "")
        if "while(true)" in condensed or "whileTrue:" in condensed or "for(;;)" in condensed:
            return ExecutionResult(
                status=SubmissionStatus.TIME_LIMIT_EXCEEDED,
                execution_time=time_limit,
                memory_usage=18200,
                error_message="Time Limit Exceeded (execution exceeded limit)"
            )

        if "# mock_accepted" in source_code:
            clean_expected = expected_output.strip()
            return ExecutionResult(
                status=SubmissionStatus.ACCEPTED,
                execution_time=0.03,
                memory_usage=5120,
                stdout=clean_expected + "\n"
            )

        # 2. Real Python execution when language is Python
        if language == 'python':
            start_t = time.time()
            try:
                proc = subprocess.run(
                    [sys.executable, "-c", source_code],
                    input=stdin or "",
                    capture_output=True,
                    text=True,
                    timeout=min(float(time_limit), 5.0)
                )
                elapsed = max(0.01, round(time.time() - start_t, 3))
                stdout_val = proc.stdout or ""
                stderr_val = proc.stderr or ""

                if proc.returncode != 0:
                    status = (
                        SubmissionStatus.COMPILATION_ERROR
                        if "SyntaxError" in stderr_val
                        else SubmissionStatus.RUNTIME_ERROR
                    )
                    return ExecutionResult(
                        status=status,
                        execution_time=elapsed,
                        memory_usage=4096,
                        stderr=stderr_val,
                        compile_output=stderr_val if status == SubmissionStatus.COMPILATION_ERROR else None,
                        stdout=stdout_val
                    )

                clean_stdout = stdout_val.strip()
                clean_expected = (expected_output or "").strip()

                if clean_stdout == clean_expected:
                    return ExecutionResult(
                        status=SubmissionStatus.ACCEPTED,
                        execution_time=elapsed,
                        memory_usage=4096,
                        stdout=stdout_val
                    )
                else:
                    return ExecutionResult(
                        status=SubmissionStatus.WRONG_ANSWER,
                        execution_time=elapsed,
                        memory_usage=4096,
                        stdout=stdout_val
                    )
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    status=SubmissionStatus.TIME_LIMIT_EXCEEDED,
                    execution_time=float(time_limit),
                    memory_usage=18200,
                    error_message=f"Time Limit Exceeded ({time_limit}s exceeded)"
                )
            except Exception as e:
                return ExecutionResult(
                    status=SubmissionStatus.INTERNAL_ERROR,
                    execution_time=0.01,
                    memory_usage=2048,
                    error_message=str(e)
                )

        # 3. For compiled languages (cpp, c) and javascript without isolated sandbox:
        if language in ['cpp', 'c']:
            if "main(" not in source_code:
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="error: 'main' function was not declared in this scope."
                )
            if "int main() {" not in source_code and "int main(" not in source_code:
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="error: syntax error before token"
                )

        # Fallback for mock test fixtures in CI/pytest
        clean_expected = expected_output.strip()
        return ExecutionResult(
            status=SubmissionStatus.ACCEPTED,
            execution_time=0.03,
            memory_usage=5120,
            stdout=clean_expected + "\n"
        )

