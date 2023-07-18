import os
from dotenv import load_dotenv

import requests
import jinja2
#the background worker is a sepaate procces from you flask app so is not gona run with app.py is running
load_dotenv()

domain = os.getenv("MAIL_DOMAIN") 
mail_gun_api = os.getenv("MAILGUN_API_KEY")   


template_loader = jinja2.FileSystemLoader('templates')
template_env = jinja2.Environment(loader= template_loader)
def render_template (template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
        
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", mail_gun_api),
         data={"from": "Illia Natiahin <IlliaNatiahin@mydomain>",
               "to": [to],
               "subject": subject,
               "text": body,
                "html": html })

def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f'Hi {username} you have successfully signed up to the Stores REST API!',
        render_template('email/action.html', username= username)
        )