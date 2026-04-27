import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Utilities import configReader


def send_email_with_allure_link(test_status: str, log_file_path: str = None):
    """
    :param test_status:
    :param log_file_path:
    """

    # ============================================================
    # 🔐 CREDENCIALES (ENV FIRST, FALLBACK LOCAL)
    # ============================================================

    sender_email = os.getenv("EMAIL_SENDER") or "juangoq12345@gmail.com"
    receiver_email = os.getenv("EMAIL_RECEIVER") or "juanquicenoutd@gmail.com"
    app_password = os.getenv("EMAIL_APP_PASSWORD") or configReader.readConfig("credentials", "gmailPassw")

    if not os.getenv("EMAIL_SENDER"):
        print("⚠️ EMAIL_SENDER no definido, usando valor local")

    if not os.getenv("EMAIL_RECEIVER"):
        print("⚠️ EMAIL_RECEIVER no definido, usando valor local")

    if not os.getenv("EMAIL_APP_PASSWORD"):
        print("⚠️ EMAIL_APP_PASSWORD no definido, usando valor local")

    # ============================================================
    # 📧 CONTENIDO DEL EMAIL
    # ============================================================
    allure_url = "https://jqperficient.github.io/automation-reports/"
    test_status = test_status.upper()

    if test_status == "PASSED":
        subject = "✅ Automation Report – Regression"
        body = f"""
Hola,

✅ La ejecución de pruebas automáticas FINALIZÓ EXITOSAMENTE.

👉 Reporte Allure:
{allure_url}

Se adjunta el log de la ejecución.

Saludos,
Automation Framework
"""
    else:
        subject = "❌ Automation Report – Regression"
        body = f"""
Hola,

❌ La ejecución de pruebas automáticas FINALIZÓ CON ERRORES.

Se adjunta el log de la ejecución para análisis.

Saludos,
Automation Framework
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # ============================================================
    # 📎 ADJUNTAR LOG
    # ============================================================
    if log_file_path and os.path.exists(log_file_path):
        with open(log_file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(log_file_path)}"'
        )
        msg.attach(part)
        print(f"📎 Log adjuntado correctamente: {log_file_path}")
    else:
        print(f"⚠️ Log NO encontrado, se enviará email sin adjunto: {log_file_path}")

    # ============================================================
    # 📤 ENVÍO
    # ============================================================
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

    print(f"✅ Email enviado con estado: {test_status}")
