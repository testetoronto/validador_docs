from flask import Flask, request, redirect, send_from_directory
import os
import uuid
import qrcode

app = Flask(__name__, static_folder='public', static_url_path='')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return redirect('/index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf = request.files['pdf']
    if pdf:
        filename = f"{uuid.uuid4()}.pdf"
        path = os.path.join(UPLOAD_FOLDER, filename)
        pdf.save(path)

        # Gerar QR Code apontando para o PDF
        link = f"https://SEU_DOMINIO/uploads/{filename}"
        qr = qrcode.make(link)
        qr_path = os.path.join(UPLOAD_FOLDER, filename + '.png')
        qr.save(qr_path)

        return f"Documento enviado com sucesso! <br><a href='{link}'>Acessar Documento</a><br><img src='/uploads/{filename}.png'>"
    return "Erro ao enviar."

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
