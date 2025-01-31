from infra.services.email.email_sender import EmailSender
from infra.services.email.email_template import EmailTemplate
from app.models.entities.user import User

emailSender = EmailSender()

def test_send_email():
    user = User(username="Kaique", email="khs@ic.ufal.br")
    subject = f"Bem-vindo à nossa plataforma, {user.username}!"

    html_content = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f7fafc;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        max-width: 600px;
                        margin: 0 auto;
                    }}
                    h1 {{
                        color: #fb923c;  /* Orange-400 */
                    }}
                    p {{
                        color: #4a4a4a;
                        line-height: 1.6;
                    }}
                    .highlight {{
                        background-color: #fef3c7;
                        padding: 10px;
                        border-radius: 5px;
                        color: #fb923c;  /* Orange-400 */
                    }}
                    ul {{
                        padding-left: 20px;
                    }}
                    ul li {{
                        margin-bottom: 10px;
                    }}
                    a {{
                        color: #fb923c;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 12px;
                        color: #a1a1a1;  /* Gray-200 */
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Olá, {user.username}!</h1>
                    <p>Bem-vindo à nossa plataforma. Estamos felizes em tê-lo conosco!</p>
                    <p class="highlight"><strong>O que você pode fazer agora:</strong></p>
                    <ul>
                        <li>Acessar seu <a href="https://example.com">painel de usuário</a></li>
                        <li>Explorar nossos serviços</li>
                        <li>Entrar em contato com nosso suporte</li>
                    </ul>
                    <p>Atenciosamente,</p>
                    <p>Equipe</p>
                    <div class="footer">
                        <p>Este é um e-mail automático, por favor, não responda.</p>
                    </div>
                </div>
            </body>
        </html>
        """
    
    email_template = EmailTemplate("", user.email, subject)
    email_template.set_body(html_content)
    
    res = emailSender.send(user.email, subject, email_template.as_string())
    
    assert res == True