class Handler:
    def __init__(self, client):
        self.client = client

    def route(self, req):
        return