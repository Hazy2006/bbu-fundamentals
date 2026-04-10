class UndoRedoException(Exception):
    pass

class FunctionCall:
    def __init__(self, function_ref, *function_params, **function_kwargs):
        """
        Reserved kw: param_repr -> a human readable description used only for describe()
        All other kwargs are forwarded to the wrapped function.
        """
        self._func_ref = function_ref
        self._params = function_params
        self._param_repr = function_kwargs.pop('param_repr', None)
        self._kwargs = function_kwargs

    def __call__(self):
        return self._func_ref(*self._params, **self._kwargs)

    def describe(self):
        if self._param_repr:
            return self._param_repr
        name = getattr(self._func_ref, "__name__", repr(self._func_ref))
        params = ", ".join(repr(p) for p in self._params)
        return f"{name}({params})"

class Operation:
    def __init__(self, undo_call, redo_call):
        self._undo_call = undo_call
        self._redo_call = redo_call

    def undo(self):
        # perform undo and return a human-readable description (if available)
        res = self._undo_call()
        if hasattr(self._undo_call, "describe"):
            return self._undo_call.describe()
        return None

    def redo(self):
        res = self._redo_call()
        if hasattr(self._redo_call, "describe"):
            return self._redo_call.describe()
        return None

class CascadedOperation:
    def __init__(self):
        self._operations = []

    def add(self, operation):
        self._operations.append(operation)

    def undo(self):
        """
        Undo should restore state safely.
        We record [GradesOp, StudentOp].
        To restore, we must restore Student (Op 2) FIRST, then Grades (Op 1).
        So we iterate in REVERSE order.
        """
        descriptions = []
        for op in reversed(self._operations):      # CHANGED: Reverse order
            d = op.undo()
            if d:
                descriptions.append(d)
        return "; ".join(descriptions) if descriptions else None

    def redo(self):
        """
        Redo must re-apply the original actions.
        We want to remove Grades (Op 1) FIRST, then Student (Op 2).
        So we iterate in FORWARD order.
        """
        descriptions = []
        for op in self._operations:
            d = op.redo()
            if d:
                descriptions.append(d)
        return "; ".join(descriptions) if descriptions else None

class UndoRedoService:
    def __init__(self):
        self._history = []
        self._index = -1

    def record(self, operation):
        # Discard any "redo" history if we make a new change
        self._history = self._history[:self._index + 1]
        self._history.append(operation)
        self._index += 1

    def undo(self):
        if self._index < 0:
            raise UndoRedoException("No more undos.")
        operation = self._history[self._index]
        desc = operation.undo()
        self._index -= 1
        return desc or "Undo performed."

    def redo(self):
        if self._index >= len(self._history) - 1:
            raise UndoRedoException("No more redos.")
        self._index += 1
        operation = self._history[self._index]
        desc = operation.redo()
        return desc or "Redo performed."

    def restart(self):
        """
        Clears the undo/redo history.
        Useful to call after automatic data generation so the user
        doesn't have to undo many system actions.
        """
        self._history = []
        self._index = -1