from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic_settings import BaseSettings
from typing import ClassVar


# Calculer le temps restant jusqu'à la fin de la journée
def get_minutes_until_end_of_day():
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_left = start_of_day + timedelta(days=1) - now
    return time_left.total_seconds() // 60


class Settings(BaseSettings):
    PROJECT_NAME: str = "TOC TOC MEDOC"
    PROJECT_VERSION: str = "1.42.27"
    #DATABASE_URL: str = "postgresql://root:root@db:5432/toctocmedoc_db"
    DATABASE_URL: str = "postgresql://root:root@51.68.46.67:5432/toctocmedoc_db"
    SECRET_KEY: str = "25a4785f40a94febf6f3b97ccd9e5aa0aaf5c5e2cbbc56b008549b9eb0d03d00"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: float = get_minutes_until_end_of_day()
    pwd_context: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")
    X_API_KEY: str = "fd188670-4871-4b16-92f4-cc30e1feab7b"
    # EPG_SUPERVISOR_ADDRESS = "http://127.0.0.1:5003"
    EPG_SUPERVISOR_ADDRESS: str = "https://51.68.46.67:5003"
    ADMIN_PANEL: str = "https://epharma-panel.srv557357.hstgr.cloud"


    # API MyPayGa
    success_url: str = "https://51.68.46.67:8000/my_pay_ga/success_url"
    callback_url: str = "https://51.68.46.67:8000/my_pay_ga/callback_url"
    fail_url: str = "https://51.68.46.67:8000/my_pay_ga/fail_url"
    # apikey = "stest_jLUmg7YiNfxsQ2ag1YIb76slZjqmFlz3L4u4SgB7Jwm1dBptqp"
    apikey: str = "sprod_HVvbdtzUcZo8HwIs1XToRfW5GqALFLPwHARNAfI1yylESgiJNu"
    country: str = "GA"
    type: str = "mobile_money"
    # Lien de paiement
    link_payment: str = "https://api.mypayga.com/v1/payment"

    # MongoDB settings
    MONGODB_URL: str = "mongodb://51.68.46.67:27017"
    MONGODB_DB_NAME: str = "ttm_db"

    class Config:
        env_file = ".env"


settings = Settings()
