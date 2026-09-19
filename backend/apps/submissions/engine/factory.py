"""
Execution engine factory.
Automatically picks Judge0 when online; falls back to DevFallbackEngine in local development.
"""
import sys
from django.conf import settings
from .base import AbstractExecutionEngine
from .judge0 import Judge0Engine
from .dev_engine import DevFallbackEngine


def get_execution_engine() -> AbstractExecutionEngine:
    judge0 = Judge0Engine()
    if judge0.is_available():
        return judge0
    if settings.DEBUG or 'pytest' in sys.modules or 'test' in sys.argv:
        return DevFallbackEngine()
    raise RuntimeError('Code execution service temporarily unavailable.')

