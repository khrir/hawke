from flask import Flask, render_template
from routes.routes import register_routes
from dotenv import load_dotenv
import os, ssl, ngrok, logging

load_dotenv()

app = Flask(__name__, template_folder='app/views', static_folder='static')

# Registrar as rotas
register_routes(app)
app.secret_key = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrão')

logging.basicConfig(level=logging.INFO)
# listener = ngrok.werkzeug_develop()

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, ssl_context=("hawke/infra/certs/server.crt", "hawke/infra/certs/server.key"), host='0.0.0.0', port=8443)