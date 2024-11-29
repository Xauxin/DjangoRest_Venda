class fieldError(Exception):
    def __init__(self, msg, value=None):
        if value is None:
            value = {}
        self.msg = msg
        self.value = value
        super().__init__()