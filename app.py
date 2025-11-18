from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
from io import BytesIO
from typing import Optional

load_dotenv()

app = FastAPI(title="Classificador de Emails")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chave_api = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=chave_api)

class EmailAnalysisResponse(BaseModel):
    categoria: str
    resposta_sugerida: str
    confianca: str

def extrair_texto_do_pdf(pdf_file: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Errp ao processar PDF: {str(e)}")
    
def classificar_email(email_text: str) -> EmailAnalysisResponse:
    classification_prompt = f"""Você é um assistente de IA especializado em classificar emails do setor financeiro.

Analise o email abaixo e classifique-o em uma das seguintes categorias:
- PRODUTIVO: Emails que requerem uma ação ou resposta específica (solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, pedidos de informação, reclamações, etc.)
- IMPRODUTIVO: Emails que não necessitam de uma ação imediata (mensagens de felicitações, agradecimentos, mensagens de final de ano, etc.)

Email:
---
{email_text}
---

Responda APENAS com uma das palavras: PRODUTIVO ou IMPRODUTIVO"""
    
    try:
        classification_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de emails corporativos do setor financeiro."},
                {"role": "user", "content": classification_prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )

        categoria = classification_response.choices[0].message.content.strip().upper()

        if categoria not in ["PRODUTIVO", "IMPRODUTIVO"]:
            categoria = "PRODUTIVO"
        
        if categoria == "PRODUTIVO":
            response_prompt = f"""
Você é um assistente de atendimento de uma empresa financeira.

Com base no email abaixo, gere uma resposta profissional e cordial que:
1. Reconheça o recebimento da solicitação
2. Indique que o caso está sendo analisado
3. Forneça um prazo estimado de resposta (24-48 horas úteis)
4. Mantenha um tom formal mas acolhedor

Email recebido:
---
{email_text}
---

Escreva APENAS a resposta sugerida, sem explicações adicionais."""
        else:
            response_prompt = f"""Você é um assistente de atendimento de uma empresa financeira.

Com base no email abaixo (que é uma mensagem de cortesia/agradecimento), gere uma resposta breve, cordial e profissional.

Email recebido:
---
{email_text}
---

Escreva APENAS a resposta sugerida, sem explicações adicionais."""
        response_generation = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de atendimento profissional de uma instituição financeira."},
                {"role": "user", "content": response_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        resposta_sugerida = response_generation.choices[0].message.content.strip()

        confianca = "Alta"

        return EmailAnalysisResponse(
            categoria=categoria,
            resposta_sugerida=resposta_sugerida,
            confianca=confianca
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise com OpenAI: {str(e)}")
    
@app.post("/analise", response_model=EmailAnalysisResponse)
async def analyze_email(
    email_content: Optional[str] = Form(None),
    email_file: Optional[UploadFile] =  File(None)
):
    text_to_analyze = ""

    if email_file:
        file_content = await email_file.read()

        if email_file.filename.endswith(".pdf"):
            text_to_analyze = extrair_texto_do_pdf(file_content)
        elif email_file.filename.endswith('.txt'):
            text_to_analyze = file_content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf")
    elif email_content:
        text_to_analyze = email_content
    else:
        raise HTTPException(status_code=400, detail="Forneça um email (texto ou arquivo)")

    if not text_to_analyze or len(text_to_analyze.strip()) < 10:
        raise HTTPException(status_code=400, detail="O email está vazio ou muito curto.")
    
    result = classificar_email(text_to_analyze)

    return result

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "API funcionando corretamente"
    }

@app.get("/")
async def read_index():
    return FileResponse("index.html")