class InvalidOffer(Exception):
    def __init__(self, message="Oferta inválida"):
        self.message = message
        super().__init__(self.message)