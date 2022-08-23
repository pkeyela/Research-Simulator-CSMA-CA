# TODO classes
class RTS:
    def __init__(self):
        self.sender_id = -1
        self.type = 'rts'
        self.size = 512  # TODO

    def get_sender_id(self):
        return self.sender_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id


class CTS:
    def __init__(self):
        self.sender_id = -1
        self.type = 'cts'
        self.size = 512  # TODO

    def get_sender_id(self):
        return self.sender_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id


class DATA:
    def __init__(self):
        self.sender_id = -1
        self.type = 'data'
        self.size = 512  # TODO

    def get_sender_id(self):
        return self.sender_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id


class ACK:
    def __init__(self):
        self.sender_id = -1
        self.type = 'ack'
        self.size = 512  # TODO

    def get_sender_id(self):
        return self.sender_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id


class Empty:
    def __init__(self):
        self.type = 'unknown'