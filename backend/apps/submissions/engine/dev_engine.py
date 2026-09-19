"""
Development & testing fallback execution engine.
Emulates compilation checks and output comparison when Judge0 is not running.
"""
import time
import re
from .base import AbstractExecutionEngine, ExecutionResult
from ..models import SubmissionStatus


class DevFallbackEngine(AbstractExecutionEngine):
    """
    Safe fallback engine for local dev and pytest when Judge0 stack is offline.
    Never executes arbitrary untrusted shell code.
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

        # Language-specific syntax checking
        if language in ['cpp', 'c']:
            if "main(" not in source_code:
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="error: 'main' function was not declared in this scope."
                )
            if "syntax_error" in source_code or ("int main() {" not in source_code and "int main(" not in source_code):
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="error: syntax error before token"
                )
        elif language == 'python':
            if "syntax_error" in source_code:
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="SyntaxError: invalid syntax"
                )
        elif language == 'javascript':
            if "syntax_error" in source_code:
                return ExecutionResult(
                    status=SubmissionStatus.COMPILATION_ERROR,
                    execution_time=0.01,
                    memory_usage=1240,
                    compile_output="SyntaxError: Unexpected token"
                )

        # Time limit heuristic
        condensed = source_code.replace(" ", "")
        if "while(true)" in condensed or "whileTrue:" in condensed or "for(;;)" in condensed:
            return ExecutionResult(
                status=SubmissionStatus.TIME_LIMIT_EXCEEDED,
                execution_time=time_limit,
                memory_usage=18200,
                error_message="Time Limit Exceeded (execution exceeded limit)"
            )

        # Runtime error heuristic
        if "raise_runtime_error" in source_code or "throw " in source_code or "raise " in source_code:
            return ExecutionResult(
                status=SubmissionStatus.RUNTIME_ERROR,
                execution_time=0.02,
                memory_usage=3200,
                stderr="Runtime error: execution terminated abnormally."
            )

        # If code contains explicit hardcoded wrong answer marker for testing
        if "force_wrong_answer" in source_code:
            return ExecutionResult(
                status=SubmissionStatus.WRONG_ANSWER,
                execution_time=0.02,
                memory_usage=4500,
                stdout="wrong output\n"
            )

        # By default in dev mode for valid code: return Accepted with expected output
        clean_expected = expected_output.strip()
        return ExecutionResult(
            status=SubmissionStatus.ACCEPTED,
            execution_time=0.03,
            memory_usage=5120,
            stdout=clean_expected + "\n"
        )

