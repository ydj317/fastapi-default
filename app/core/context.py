import contextvars

trace_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default=None)
is_login_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("is_login", default=False)
username_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("username", default="")

def set_trace_id(trace_id: str):
    trace_id_ctx_var.set(trace_id)

def get_trace_id() -> str:
    return trace_id_ctx_var.get()

def set_is_login(is_login: bool):
    is_login_ctx_var.set(is_login)

def get_is_login() -> bool:
    return is_login_ctx_var.get()

def set_username(username: str):
    username_ctx_var.set(username)

def get_username() -> str:
    return username_ctx_var.get()
