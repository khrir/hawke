import mercadopago, dotenv, os

dotenv.load_dotenv()

class MercadoPagoSDK:
    def __init__(self):
        self.sdk = mercadopago.SDK(os.getenv('MP_ACCESS_TOKEN'))

    def create_preference(self, preference):
        preference_response =  self.sdk.preference().create(preference)
        return preference_response['response']
    

# Cria um item na preferência
# preference_data = {
#     "items": [
#         {
#             "title": "My Item",
#             "quantity": 1,
#             "unit_price": 75.76
#         }
#     ]
# }