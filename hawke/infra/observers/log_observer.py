from infra.writters.LogWritter import FileLogWriter

class LogObserver:
    def __init__(self):
        self.logger = FileLogWriter()

    def update(self, data):
        event = data.get('event')
        user = data.get('user')
        self.logger.purchase(f"Inscricao realizada: {event.get('id')} para o cliente {user.get('username')}")