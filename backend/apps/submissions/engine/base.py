"""
Base abstractions and data structures for code execution engines.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionResult:
    status: str  # From SubmissionStatus (ACCEPTED, WRONG_ANSWER, etc.)
    execution_time: float  # In seconds
    memory_usage: int  # In KB
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    error_message: str = ""


class AbstractExecutionEngine(ABC):
    """
    Abstract interface for executing code in an isolated sandbox.
    """

    @abstractmethod
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
        """
        Executes code against given standard input and compares with expected output.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Returns True if the execution sandbox is reachable and healthy.
        """
        pass

