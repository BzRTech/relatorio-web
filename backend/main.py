"""
main.py — API FastAPI para geração de relatórios de logradouros.
Deploy: Render.com (grátis) via Docker.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import zipfile
from relatorio import gerar_relatorio

app = FastAPI(title="Relatório de Logradouros — Eixo Engenharia")

# Permite chamadas do frontend (GitHub Pages ou qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "msg": "API Relatório de Logradouros — Eixo Engenharia"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/gerar")
async def gerar(
    municipio: str          = Form(..., description="Nome do município"),
    tabela:    UploadFile   = File(..., description="CSV, Excel ou DBF com os atributos"),
    shapefile: UploadFile   = File(..., description="ZIP com .shp + .dbf + .shx + .prj"),
    tif:       UploadFile   = File(None, description="GeoTIFF opcional como fundo do mapa"),
):
    """
    Recebe os arquivos, gera PDF + Excel e devolve um ZIP com os dois.
    """
    try:
        tabela_bytes   = await tabela.read()
        shp_bytes      = await shapefile.read()
        tif_bytes      = await tif.read() if tif else None

        pdf_bytes, excel_bytes = gerar_relatorio(
            tabela_bytes   = tabela_bytes,
            tabela_filename= tabela.filename,
            shp_bytes      = shp_bytes,
            nome_municipio = municipio.strip(),
            tif_bytes      = tif_bytes,
        )

        # Empacota PDF + Excel num único ZIP para download
        zip_buf = io.BytesIO()
        nome_safe = municipio.strip().replace(" ", "_")
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"Relatorio_Logradouros_{nome_safe}.pdf",   pdf_bytes)
            zf.writestr(f"Relatorio_Logradouros_{nome_safe}.xlsx",  excel_bytes)
        zip_buf.seek(0)

        return StreamingResponse(
            zip_buf,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="Relatorio_{nome_safe}.zip"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
