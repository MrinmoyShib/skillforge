"""
Judge0 isolated code execution engine implementation.
"""
import base64
import time
import requests
import logging
from django.conf import settings
from .base import AbstractExecutionEngine, ExecutionResult
from ..models import SubmissionStatus

logger = logging.getLogger(__name__)

# Judge0 language ID map (CE default)
JUDGE0_LANGUAGE_IDS = {
    'cpp': 54,       # C++ (GCC 9.2.0)
    'c': 50,         # C (GCC 9.2.0)
    'python': 71,    # Python (3.8.1)
    'javascript': 63 # JavaScript (Node.js 12.14.0)
}

# Judge0 status ID mapping to SkillForge SubmissionStatus
JUDGE0_STATUS_MAP = {
    3: SubmissionStatus.ACCEPTED,
    4: SubmissionStatus.WRONG_ANSWER,
    5: SubmissionStatus.TIME_LIMIT_EXCEEDED,
    6: SubmissionStatus.COMPILATION_ERROR,
    7: SubmissionStatus.RUNTIME_ERROR,   # SIGSEGV
    8: SubmissionStatus.RUNTIME_ERROR,   # SIGXFSZ
    9: SubmissionStatus.RUNTIME_ERROR,   # SIGFPE
    10: SubmissionStatus.RUNTIME_ERROR,  # SIGABRT
    11: SubmissionStatus.RUNTIME_ERROR,  # NZEC
    12: SubmissionStatus.RUNTIME_ERROR,  # Other
    13: SubmissionStatus.INTERNAL_ERROR, # Internal Error
    14: SubmissionStatus.INTERNAL_ERROR, # Exec Format Error
}


def _b64_encode(value: str) -> str:
    if not value:
        return ""
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def _b64_decode(value: str) -> str:
    if not value:
        return ""
    try:
        return base64.b64decode(value.encode('utf-8')).decode('utf-8', errors='replace')
    except Exception:
        return value


class Judge0Engine(AbstractExecutionEngine):
    """
    Communicates with a self-hosted Judge0 CE server via REST API.
    """
    def __init__(self, base_url: str = None, auth_token: str = None):
        self.base_url = (base_url or getattr(settings, 'JUDGE0_URL', 'http://judge0-server:2358')).rstrip('/')
        self.auth_token = auth_token or getattr(settings, 'JUDGE0_AUTH_TOKEN', '')

    def _get_headers(self) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.auth_token:
            headers['X-Auth-Token'] = self.auth_token
        return headers

    def is_available(self) -> bool:
        """
        Pings Judge0 system info or languages endpoint to test connectivity.
        """
        try:
            url = f"{self.base_url}/about"
            resp = requests.get(url, headers=self._get_headers(), timeout=2.0)
            return resp.status_code == 200
        except Exception:
            return False

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
        lang_id = JUDGE0_LANGUAGE_IDS.get(language, 54)
        url = f"{self.base_url}/submissions?base64_encoded=true&wait=false"

        payload = {
            "source_code": _b64_encode(source_code),
            "language_id": lang_id,
            "stdin": _b64_encode(stdin),
            "expected_output": _b64_encode(expected_output.strip()),
            "cpu_time_limit": time_limit,
            "wall_time_limit": time_limit * 2,
            "memory_limit": memory_limit,
        }

        try:
            resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=10.0)
            resp.raise_for_status()
            token = resp.json().get('token')
        except Exception as exc:
            logger.error(f"Failed to submit code to Judge0: {exc}")
            return ExecutionResult(
                status=SubmissionStatus.INTERNAL_ERROR,
                execution_time=0.0,
                memory_usage=0,
                error_message=f"Judge0 connection error: {str(exc)}"
            )

        # Poll for verdict (max 15 attempts, 0.8s interval)
        status_url = f"{self.base_url}/submissions/{token}?base64_encoded=true"
        for _ in range(15):
            time.sleep(0.8)
            try:
                poll_resp = requests.get(status_url, headers=self._get_headers(), timeout=5.0)
                poll_resp.raise_for_status()
                data = poll_resp.json()

                status_id = data.get('status', {}).get('id', 1)
                # 1 = In Queue, 2 = Processing
                if status_id not in (1, 2):
                    mapped_status = JUDGE0_STATUS_MAP.get(status_id, SubmissionStatus.INTERNAL_ERROR)
                    exec_time = float(data.get('time') or 0.0)
                    memory = int(data.get('memory') or 0)
                    stdout = _b64_decode(data.get('stdout') or "")
                    stderr = _b64_decode(data.get('stderr') or "")
                    compile_output = _b64_decode(data.get('compile_output') or "")

                    return ExecutionResult(
                        status=mapped_status,
                        execution_time=exec_time,
                        memory_usage=memory,
                        stdout=stdout,
                        stderr=stderr,
                        compile_output=compile_output
                    )
            except Exception as exc:
                logger.warning(f"Error while polling Judge0 for token {token}: {exc}")

        return ExecutionResult(
            status=SubmissionStatus.TIME_LIMIT_EXCEEDED,
            execution_time=time_limit,
            memory_usage=0,
            error_message="Evaluation timed out waiting for Judge0 worker."
        )

