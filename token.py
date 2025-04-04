from Jaipur.resource import Resource


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        if self.token_type in Resource.normal_resources():
            return str(self.value)
        else:
            return '?'

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.token_type == other.token_type and self.value == other.value
        return False

    def __hash__(self):
        return hash(self.token_type)