# Relatório de Logradouros — Eixo Engenharia

Sistema web para geração automatizada de relatórios de logradouros (PDF + Excel) a partir de dados tabulares e shapefiles.

**Custo: R$ 0,00/mês** — GitHub Pages (frontend) + Render.com free tier (backend)

---

## Estrutura do projeto

```
relatorio-web/
├── backend/
│   ├── main.py           # API FastAPI
│   ├── relatorio.py      # Lógica de geração do relatório
│   ├── requirements.txt  # Dependências Python
│   └── Dockerfile        # Imagem Docker com GDAL
└── frontend/
    └── index.html        # Interface web (upload + download)
```

---

## Deploy — Passo a passo

### 1. Criar repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **New repository**
3. Nome sugerido: `relatorio-logradouros`
4. Deixe como **Public** (necessário para GitHub Pages gratuito)
5. Clique em **Create repository**

Faça upload dos arquivos (ou use git):

```bash
git init
git add .
git commit -m "Primeiro commit"
git remote add origin https://github.com/SEU-USUARIO/relatorio-logradouros.git
git push -u origin main
```

---

### 2. Deploy do Backend no Render.com

1. Acesse [render.com](https://render.com) e crie uma conta gratuita (pode usar login GitHub)

2. No dashboard, clique em **New +** → **Web Service**

3. Conecte seu repositório GitHub (`relatorio-logradouros`)

4. Configure o serviço:
   | Campo | Valor |
   |-------|-------|
   | **Name** | `relatorio-eixo` (ou outro nome) |
   | **Region** | Oregon (US West) ou outra |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | **Docker** |
   | **Instance Type** | **Free** |

5. Clique em **Deploy Web Service**

6. Aguarde o build (5–10 minutos na primeira vez — GDAL é grande)

7. Após o deploy, copie a URL do serviço, que terá o formato:
   ```
   https://relatorio-eixo.onrender.com
   ```

> **Nota:** No plano gratuito do Render, o serviço "dorme" após 15 minutos sem uso.
> A primeira requisição após um período inativo pode demorar ~30–60 segundos para acordar.
> Isso é normal — o frontend mostra uma barra de progresso animada durante esse tempo.

---

### 3. Atualizar a URL no Frontend

Abra o arquivo `frontend/index.html` e altere a linha:

```js
// ANTES:
const API_URL = "https://SEU-APP.onrender.com";

// DEPOIS (use a URL real do seu serviço Render):
const API_URL = "https://relatorio-eixo.onrender.com";
```

Salve o arquivo e faça commit/push para o GitHub:

```bash
git add frontend/index.html
git commit -m "Atualiza URL da API"
git push
```

---

### 4. Publicar o Frontend no GitHub Pages

1. No GitHub, acesse seu repositório
2. Vá em **Settings** → **Pages** (menu lateral esquerdo)
3. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/ (root)` — ou `/frontend` se preferir
4. Clique em **Save**
5. Aguarde ~1 minuto. A URL do seu site será algo como:
   ```
   https://SEU-USUARIO.github.io/relatorio-logradouros/frontend/
   ```

> **Dica:** Se selecionar `/(root)` como pasta, o GitHub Pages servirá `index.html` na raiz.
> Para evitar conflito, mova `frontend/index.html` para a raiz do repositório se quiser URL mais limpa.

---

## Uso do sistema

1. Acesse a URL do GitHub Pages no navegador
2. Preencha o **nome do município**
3. Faça upload da **tabela de logradouros** (CSV, Excel ou DBF)
4. Faça upload do **shapefile das vias** (ZIP contendo .shp + .dbf + .shx + .prj)
5. Opcionalmente, faça upload de uma **ortofoto GeoTIFF** (.tif) como fundo do mapa
   - Se não enviar, o sistema usa Google Satellite automaticamente
6. Clique em **⚡ Gerar Relatório**
7. Aguarde o processamento (30–120 segundos)
8. Clique em **⬇️ Baixar PDF + Excel (.zip)**

---

## Formatos aceitos

| Arquivo | Formatos |
|---------|----------|
| Tabela de logradouros | `.csv`, `.xlsx`, `.xls`, `.dbf` |
| Shapefile | `.zip` com `.shp` + `.dbf` + `.shx` + `.prj` |
| Ortofoto (opcional) | `.tif`, `.tiff` (GeoTIFF) |

---

## O relatório gerado

O arquivo `.zip` baixado contém:

- **PDF** com 9 páginas:
  1. Capa com nome do município
  2. Visão geral (totais e indicadores)
  3. Gráfico de pavimentação por tipo
  4. Gráfico de status das vias
  5. Gráfico por bairro
  6. Gráfico por setor
  7. Mapa de calor (heatmap de comprimentos)
  8. Mapa georreferenciado com shapefile sobreposto
  9. Tabela cruzada Setor × Tipo de pavimentação

- **Excel** (.xlsx) com 6 abas:
  1. Resumo Geral
  2. Pavimentação
  3. Status
  4. Por Setor
  5. Por Bairro
  6. Dados Completos

---

## Paleta de cores

| Tipo | Cor |
|------|-----|
| Leito Natural | 🔴 Vermelho `#E53935` |
| Paralelepípedo | 🟢 Verde `#43A047` |
| Intertravado | 🔵 Azul `#1E88E5` |
| Asfalto | 🟦 Azul marinho `#0D47A1` |

---

## Variáveis de ambiente (opcionais)

Não há variáveis de ambiente obrigatórias. O sistema funciona sem configuração adicional.

Se quiser restringir as origens CORS (recomendado em produção), edite `backend/main.py`:

```python
# Trocar allow_origins=["*"] por:
allow_origins=["https://SEU-USUARIO.github.io"],
```

---

## Solução de problemas

**"Erro ao gerar relatório" no frontend**
- Verifique se a URL `API_URL` no `index.html` está correta
- Abra o Console do navegador (F12) para ver o erro detalhado
- Acesse `https://SEU-APP.onrender.com/health` — deve retornar `{"status":"healthy"}`

**O Render demora muito para responder**
- Normal no plano gratuito após inatividade (cold start de ~30–60s)
- O frontend mostra progresso animado — aguarde

**Shapefile não reconhecido**
- O ZIP deve conter os 4 arquivos: `.shp`, `.dbf`, `.shx`, `.prj`
- Não coloque o shapefile dentro de subpastas dentro do ZIP

**CSV com caracteres errados (acentos)**
- O sistema testa automaticamente encodings `utf-8`, `latin-1` e `cp1252`
- Se ainda assim houver erro, salve o CSV com encoding UTF-8 no Excel

**GeoTIFF não usado como fundo**
- O TIF deve ter CRS definido (georeferenciado)
- Se o TIF e o shapefile estiverem em CRS diferentes, o sistema faz a reprojeção automaticamente

---

## Requisitos técnicos (para rodar localmente)

```bash
# Instalar GDAL (Linux/Mac) ou usar Docker
pip install -r backend/requirements.txt

# Rodar backend localmente
cd backend
uvicorn main:app --reload --port 8000

# No frontend/index.html, usar:
# const API_URL = "http://localhost:8000";
```

Com Docker:

```bash
cd backend
docker build -t relatorio-eixo .
docker run -p 8000:8000 relatorio-eixo
```

---

## Créditos

Desenvolvido para uso interno da **Eixo Engenharia e Projetos**.
