import gspread
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os
import json
import uuid
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === CONFIG ===
SUPABASE_URL = "https://ycmedsqrgxitwjoudqkc.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PASTA_ID = "1dtYbWuL_CZ-hQn2mh75kDrAufQhT0HqZ"
DEBUG = True

# === CREDENCIAIS DO GOOGLE ===
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_K"])
except KeyError:
    print("❌ Variável de ambiente 'GOOGLE_SERVICE_ACCOUNT_K' não encontrada.")
    exit(1)

creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)

print("🕒 Início:", datetime.now())
planilha = gc.open("ABF Express - NSW/ACT Allocations")
aba = planilha.worksheet("ALLOCATIONS")
dados = aba.get_all_values()[3:]
print(f"📄 Linhas extraídas: {len(dados)}")

# === FILTRAGEM E DATAFRAME ===
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
df = df[df['Store #'] != '']

if df.empty:
    print("⚠️ Nenhum dado válido.")
    exit(0)

# === SHIFT E DATA ===
agora = datetime.now()
df["extraction_date"] = agora.strftime("%Y-%m-%d %H:%M:%S")


def determinar_shift(horario):
    try:
        return "AM" if datetime.strptime(horario.strip(),
                                         "%H:%M").hour < 12 else "PM"
    except:
        return "AM"


df["shift"] = df["Start Time"].apply(determinar_shift)

# === ORGANIZAÇÃO FINAL ===
df = df[[
    "Store #", "Store", "Route ID", "Drops", "KM", "Weight", "Start Time",
    "Finish Time", "Main Suburbs", "Windows", "Dock", "Total Hours", "Rego",
    "ID", "Driver", "Driver Mobile", "Max Payload", "extraction_date", "shift"
]]

# === ENVIO PARA SUPABASE ===
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print(f"🚀 Enviando {len(df)} registros para Supabase...")

sucesso = 0
falha = 0

for index, row in df.iterrows():
    registro = row.to_dict()
    registro["record_id"] = str(uuid.uuid4())
    try:
        supabase.table("allocation_database_backup").insert(registro).execute()
        sucesso += 1
    except Exception as e:
        falha += 1
        if DEBUG:
            print(f"❌ Erro no registro {index}: {e}")
            print("📦 Dados:", registro)

# === BACKUP CSV ===
nome_csv = f"{agora.strftime('%Y-%m-%d_%H-%M')}_{df['shift'].iloc[0]}_allocation.csv"
try:
    df.to_csv(nome_csv, index=False)
    media = MediaFileUpload(nome_csv, mimetype="text/csv")
    drive_service.files().create(body={
        "name": nome_csv,
        "parents": [PASTA_ID]
    },
                                 media_body=media,
                                 fields="id").execute()
    print(f"✅ Backup salvo: {nome_csv}")
except Exception as e:
    print(f"❌ Falha no backup CSV: {e}")

print("🎉 Finalizado.")
print(f"📊 Total: {len(df)} | ✅ Sucesso: {sucesso} | ❌ Falhas: {falha}")
print("🕒 Fim:", datetime.now())
