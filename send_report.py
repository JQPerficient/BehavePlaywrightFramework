import sys
from Utilities.email_sender import send_email_with_allure_link


if __name__ == "__main__":

    # ✅ Estado de la ejecución
    if len(sys.argv) < 2:
        print("⚠️ No se recibió estado, usando FAILED por defecto")
        status = "FAILED"
    else:
        status = sys.argv[1]

    # ✅ Ruta del log (segundo argumento)
    log_file_path = sys.argv[2] if len(sys.argv) > 2 else None

    # ✅ Enviar email con log adjunto
    send_email_with_allure_link(status, log_file_path)