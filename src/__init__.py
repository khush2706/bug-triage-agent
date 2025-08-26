"""Package init for src to enable `python -m src.cli`.

Auto-import tool submodules to ensure decorators register tools at startup.
"""

# Trigger registration of tools via decorators
try:  # pragma: no cover - trivial import side-effects
    from .tools import classification as _t_classification  # noqa: F401
    from .tools import workflow as _t_workflow  # noqa: F401
except Exception:  # noqa: BLE001
    # Defer errors to runtime when tools are actually requested
    pass


