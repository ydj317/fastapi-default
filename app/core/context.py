import contextvars

trace_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default=None)

def set_trace_id(trace_id: str):
    trace_id_ctx_var.set(trace_id)

def get_trace_id() -> str:
    return trace_id_ctx_var.get()