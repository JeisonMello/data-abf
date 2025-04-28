import gspread
import pandas as pd
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from zoneinfo import ZoneInfo

# === CONFIGURAÇÕES ===
FOLDER_ID = "1dtYbWuL_CZ-hQn2mh75kDrAufQhT0HqZ"  # Allocation_backup
DEBUG = True

print("🕒 Início da execução:", datetime.now())

# === AUTENTICAÇÃO GOOGLE ===
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    print("🔐 Carregando credenciais do Google...")
    creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_K"])
except KeyError:
    print("❌ Variável 'GOOGLE_SERVICE_ACCOUNT_K' não encontrada.")
    exit(1)

creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)

# === LEITURA DA PLANILHA ===
planilha = gc.open("ABF Express - NSW/ACT Allocations")
aba = planilha.worksheet("ALLOCATIONS")
print("📄 Lendo dados da aba...")
dados = aba.get_all_values()[3:]

# === PROCESSAMENTO ===
dados_filtrados = [
    linha[:16] + [linha[27]] for linha in dados if len(linha) > 27
]

df = pd.DataFrame(dados_filtrados,
                  columns=[
                      "Store #", "Store", "Route ID", "Drops", "KM", "Weight",
                      "Start Time", "Finish Time", "Main Suburbs", "Windows",
                      "Dock", "Total Hours", "Rego", "ID", "Driver",
                      "Driver Mobile", "Max Payload"
                  ])

df['Store #'] = df['Store #'].astype(str).str.strip()
df = df[df['Store #'].notna() & (df['Store #'] != '')].copy()

if df.empty:
    print("⚠️ Nenhum dado válido. Encerrando.")
    exit(0)

# === ADICIONA TIMESTAMP E SHIFT ===
agora_sydney = datetime.now(ZoneInfo("Australia/Sydney"))
df["extraction_date"] = agora_sydney.strftime("%Y-%m-%d %H:%M:%S")

# Regra: 13:30 => AM, 23:30 => PM
hora = agora_sydney.hour
minuto = agora_sydney.minute
shift = "AM" if hora == 13 else "PM"
df["shift"] = shift

# === EXPORTA PARA CSV ===
filename = agora_sydney.strftime(f"%Y-%m-%d_%H-%M_{shift}_allocation.csv")
df.to_csv(filename, index=False)
print(f"💾 CSV gerado: {filename}")

# === UPLOAD PARA GOOGLE DRIVE ===
file_metadata = {
    "name": filename,
    "parents": [FOLDER_ID],
    "mimeType": "application/vnd.google-apps.file"
}
media = MediaFileUpload(filename, mimetype="text/csv")

uploaded = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields="id").execute()

print(f"✅ Upload concluído! ID do arquivo: {uploaded.get('id')}")
print("🏁 Fim da execução:", datetime.now())
