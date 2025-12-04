from . import Settings
from ..Schema import UserSchema


def send_password(password: str, to_email: str, user: UserSchema.Read,
                  subject="Réinitialisation du mot de passe @TOC TOC MEDOC", body=""):
    html = f"""
        <html>
            <body>
                <h1>Réinitialisation du mot de passe @TOC TOC MEDOC</h1>
                <h4>Bonjour M./ Mme {user.lastname} {user.firstname}</h4>
                <p>Veuillez trouver votre nouveau mot de passe, nous vous conseillons de le changer après votre connexion: {password}</p>
                <h4>Veuillez ne pas repondre a ce mail!!!</h4>
                <p>Back Office©TOC TOC MEDOC - 2023</p>
            </body>
        </html>
    """
    Settings.send_email(to_email=to_email, subject=subject, body=body, html=html)
