# DICOM Tools

Coleção abrangente de utilitários Python para trabalhar com arquivos DICOM. Este repositório fornece **17 scripts especializados** para inspeção, descompressão, recodificação, anonimização, conversão, validação, organização, networking (PACS) e interface web, todos baseados na biblioteca [`pydicom`](https://pydicom.github.io/).

## ✨ Novidades v1.0.0

- 🎁 **Empacotamento como módulo Python** - Instale via `pip install` com comandos CLI globais
- 🌐 **Interface Web** - Visualize e processe DICOM files no navegador
- 🏥 **DICOM Networking** - Query (C-FIND) e Retrieve (C-MOVE/C-GET) de servidores PACS
- 📦 **17 comandos CLI** - Todos os scripts disponíveis como comandos globais

## 📑 Índice
- [Scripts Disponíveis](#scripts-disponíveis)
- [Instalação](#instalação)
- [Guia de Uso Detalhado](#guia-de-uso-detalhado)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Próximos Passos](#próximos-passos)
- [Licença](#licença)

---

## Scripts Disponíveis

### 📋 Inspeção e Metadados
1. **`extract_metadata.py`** - Extrai e exibe metadados DICOM detalhados organizados por categoria
2. **`dicom_info.py`** - Visualização rápida de informações resumidas de arquivos DICOM
3. **`comparar_dicom.py`** - Compara metadados entre dois arquivos DICOM

### 🔄 Conversão e Recodificação
4. **`reencode_dicom.py`** - Reescreve DICOM com transfer syntax explicit little-endian
5. **`decompress_dicom.py`** - Descomprime arquivos DICOM comprimidos
6. **`convert_to_image.py`** - Converte DICOM para PNG/JPEG com windowing adequado

### 🔒 Privacidade e Anonimização
7. **`anonymize_dicom.py`** - Anonimiza arquivos DICOM removendo PHI (HIPAA-compliant)

### ✅ Validação e Análise
8. **`validate_dicom.py`** - Valida conformidade DICOM e integridade de dados
9. **`pixel_stats.py`** - Analisa estatísticas detalhadas de pixel data com histogramas

### ✏️ Modificação e Organização
10. **`modify_tags.py`** - Modifica tags DICOM específicas (modo interativo ou batch)
11. **`organize_dicom.py`** - Organiza arquivos em hierarquia estruturada

### 🔍 Pesquisa e Filtragem
12. **`search_dicom.py`** - Pesquisa arquivos DICOM por critérios de metadados

### 🎞️ Multi-frame
13. **`split_multiframe.py`** - Divide DICOM multi-frame em arquivos single-frame

### 📦 Processamento em Lote
14. **`batch_process.py`** - Processa múltiplos arquivos com várias operações

### 🌐 DICOM Networking (NOVO!)
15. **`dicom_query.py`** - Query PACS usando C-FIND (pesquisa de estudos)
16. **`dicom_retrieve.py`** - Retrieve de PACS usando C-MOVE/C-GET (busca de imagens)

### 🖥️ Interface Web (NOVO!)
17. **`web_interface.py`** - Servidor web Flask para visualização e processamento DICOM

---

## Instalação

### 🚀 Instalação Rápida (Módulo Python)

```bash
# Instalar do repositório Git
pip install git+https://github.com/ThalesMMS/Dicom-Tools.git

# Ou instalar localmente
git clone https://github.com/ThalesMMS/Dicom-Tools.git
cd Dicom-Tools
pip install .

# Instalar em modo desenvolvimento
pip install -e .
```

Após a instalação, **todos os scripts estarão disponíveis como comandos CLI globais**:

```bash
dicom-info arquivo.dcm
dicom-anonymize entrada.dcm
dicom-web  # Inicia interface web
dicom-query -H pacs.server.com -p 11112 --patient-name "Silva*"
```

### 📋 Requisitos

- **Python 3.9 ou superior**
- **pydicom** >= 2.3.0 - Biblioteca core para DICOM
- **numpy** >= 1.20.0 - Processamento de pixel data
- **Pillow** >= 9.0.0 - Conversão de imagens
- **pynetdicom** >= 2.0.0 - DICOM networking (C-FIND, C-MOVE, C-GET)
- **flask** >= 2.0.0 - Interface web
- **flask-cors** >= 3.0.0 - CORS para web

### 🛠️ Instalação Manual (Scripts Standalone)

Se preferir usar scripts Python diretamente sem instalar o módulo:

```bash
# Clonar repositório
git clone https://github.com/ThalesMMS/Dicom-Tools.git
cd Dicom-Tools

# Criar ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar scripts diretamente
python DICOM_reencoder/dicom_info.py arquivo.dcm
```

### 📦 Comandos CLI Instalados

Após `pip install`, 17 comandos estarão disponíveis:

| Comando | Função |
|---------|--------|
| `dicom-extract-metadata` | Extração de metadados |
| `dicom-info` | Informações resumidas |
| `dicom-compare` | Comparação de arquivos |
| `dicom-reencode` | Recodificação |
| `dicom-decompress` | Descompressão |
| `dicom-to-image` | Conversão para PNG/JPEG |
| `dicom-anonymize` | Anonimização |
| `dicom-validate` | Validação |
| `dicom-pixel-stats` | Estatísticas de pixels |
| `dicom-modify` | Modificação de tags |
| `dicom-organize` | Organização de arquivos |
| `dicom-search` | Pesquisa |
| `dicom-split-multiframe` | Divisão multi-frame |
| `dicom-batch` | Processamento em lote |
| **`dicom-query`** | **Query PACS (C-FIND)** |
| **`dicom-retrieve`** | **Retrieve de PACS (C-MOVE/C-GET)** |
| **`dicom-web`** | **Interface Web** |

📖 **Guia completo de instalação:** [INSTALLATION.md](INSTALLATION.md)

---

## Guia de Uso Detalhado

### 📋 Inspeção e Metadados

#### 1. `extract_metadata.py` - Extração Detalhada de Metadados

Extrai e exibe metadados DICOM organizados em categorias (Paciente, Estudo, Série, Imagem, Equipamento, etc.).

```bash
# Extrair metadados de um arquivo específico
python DICOM_reencoder/extract_metadata.py arquivo.dcm

# Usar arquivo padrão (1.dcm)
python DICOM_reencoder/extract_metadata.py
```

**Saída:** Informações organizadas sobre Paciente, Estudo, Série, Imagem, Equipamento, Parâmetros de Aquisição, Pixel Data e Transfer Syntax.

---

#### 2. `dicom_info.py` - Informações Resumidas

Exibe um resumo conciso de arquivos DICOM, ideal para inspeção rápida.

```bash
# Informações básicas
python DICOM_reencoder/dicom_info.py arquivo.dcm

# Informações detalhadas (verbose)
python DICOM_reencoder/dicom_info.py arquivo.dcm --verbose

# Comparar dois arquivos
python DICOM_reencoder/dicom_info.py arquivo1.dcm --compare arquivo2.dcm
```

**Recursos:**
- Resumo de Patient, Study, Series e Image
- Informações de Transfer Syntax
- Modo verbose para metadados de equipamento e UIDs
- Comparação lado a lado de arquivos

---

#### 3. `comparar_dicom.py` - Comparação de Metadados

Compara metadados entre dois arquivos DICOM e destaca diferenças.

```bash
python DICOM_reencoder/comparar_dicom.py
```

**Nota:** Por padrão lê `1.dcm` e `2.dcm`. Edite o script para usar nomes diferentes.

**Saída:** Tabela comparativa com campos-chave e marcadores de diferença.

---

### 🔄 Conversão e Recodificação

#### 4. `reencode_dicom.py` - Recodificação

Reescreve arquivo DICOM com Explicit VR Little Endian transfer syntax.

```bash
python DICOM_reencoder/reencode_dicom.py
```

**Entrada:** `1.dcm`
**Saída:** `1_reencoded.dcm`

---

#### 5. `decompress_dicom.py` - Descompressão

Força descompressão de DICOM e salva versão descomprimida compatível com visualizadores legados.

```bash
python DICOM_reencoder/decompress_dicom.py
```

**Entrada:** `1.dcm`
**Saída:** `1_decompressed.dcm`

**Recursos:**
- Detecta automaticamente se imagem está comprimida
- Atualiza Transfer Syntax UID para uncompressed
- Compatível com OsiriX e visualizadores similares

---

#### 6. `convert_to_image.py` - Conversão para Imagem

Converte DICOM para formatos de imagem padrão (PNG, JPEG) com windowing apropriado.

```bash
# Converter para PNG (padrão)
python DICOM_reencoder/convert_to_image.py arquivo.dcm

# Converter para JPEG
python DICOM_reencoder/convert_to_image.py arquivo.dcm jpeg

# Especificar arquivo de saída
python DICOM_reencoder/convert_to_image.py arquivo.dcm png saida.png

# Converter todos os frames de multi-frame
python DICOM_reencoder/convert_to_image.py multiframe.dcm png --all-frames
```

**Recursos:**
- Windowing automático ou baseado em tags DICOM
- Suporte para MONOCHROME1 e MONOCHROME2
- Processa imagens single-frame e multi-frame
- Qualidade JPEG configurável

---

### 🔒 Privacidade e Anonimização

#### 7. `anonymize_dicom.py` - Anonimização HIPAA-Compliant

Remove ou substitui informações identificáveis de pacientes (PHI) mantendo integridade da imagem.

```bash
# Anonimizar arquivo (cria arquivo_anonymized.dcm)
python DICOM_reencoder/anonymize_dicom.py arquivo.dcm

# Especificar arquivo de saída
python DICOM_reencoder/anonymize_dicom.py entrada.dcm saida_anon.dcm
```

**Recursos:**
- Remove/substitui informações do paciente (Nome, ID, Data de Nascimento, etc.)
- Anonimiza médicos e instituição
- Gera IDs anônimos consistentes usando hash
- Desloca datas preservando relações temporais
- Regenera UIDs (Study, Series, SOP Instance)
- Remove tags privadas do fabricante
- Mantém metadados técnicos necessários

**PHI Removido:**
- Patient Name, ID, Birth Date, Address, Phone
- Referring Physician, Operators Name
- Institution Name, Address
- Study/Series dates (shifted)
- Private manufacturer tags

---

### ✅ Validação e Análise

#### 8. `validate_dicom.py` - Validação Completa

Valida arquivos DICOM quanto a conformidade e integridade.

```bash
python DICOM_reencoder/validate_dicom.py arquivo.dcm
```

**Verificações:**
- ✓ Estrutura do arquivo e conformidade DICOM
- ✓ Presença de tags obrigatórias (Type 1 e Type 2)
- ✓ Formato e validade de UIDs
- ✓ Consistência de pixel data (dimensões, atributos)
- ✓ Validação de formato de datas e horários
- ✓ Verificação de Transfer Syntax
- ✓ File Meta Information Header

**Saída:** Relatório detalhado com informações, avisos e erros.

---

#### 9. `pixel_stats.py` - Estatísticas de Pixel Data

Analisa e exibe estatísticas detalhadas de valores de pixel com suporte para histogramas.

```bash
# Estatísticas básicas
python DICOM_reencoder/pixel_stats.py imagem.dcm

# Com histograma
python DICOM_reencoder/pixel_stats.py imagem.dcm --histogram

# Frame específico de multi-frame
python DICOM_reencoder/pixel_stats.py multiframe.dcm --frame 5

# Comparar dois arquivos
python DICOM_reencoder/pixel_stats.py arquivo1.dcm --compare arquivo2.dcm
```

**Estatísticas Fornecidas:**
- Min, Max, Range, Mean, Median
- Standard Deviation, Variance
- Percentis (1º, 5º, 25º, 50º, 75º, 95º, 99º)
- IQR (Interquartile Range)
- Total de pixels, valores únicos
- Contagem e porcentagem de pixels zero
- Histograma visual em texto (20 bins padrão)

**Modo Comparação:**
- Compara estatísticas entre dois arquivos
- Detecta se pixel data é idêntico
- Calcula diferenças absolutas médias e máximas

---

### ✏️ Modificação e Organização

#### 10. `modify_tags.py` - Modificação de Tags

Modifica tags DICOM específicas com modo interativo ou batch.

```bash
# Modo interativo
python DICOM_reencoder/modify_tags.py arquivo.dcm

# Modo batch com tags específicas
python DICOM_reencoder/modify_tags.py arquivo.dcm -t PatientName="Doe^John" -t Modality=CT

# Especificar arquivo de saída
python DICOM_reencoder/modify_tags.py arquivo.dcm -o saida.dcm -t PatientID=12345

# Listar todas as tags do arquivo
python DICOM_reencoder/modify_tags.py arquivo.dcm --list-tags
```

**Recursos:**
- **Modo Interativo:** Interface guiada para modificar tags
- **Modo Batch:** Modificações via linha de comando
- **List Tags:** Visualiza todas as tags disponíveis
- Suporta adição de tags inexistentes
- Validação de modificações

---

#### 11. `organize_dicom.py` - Organização Estruturada

Organiza arquivos DICOM em hierarquia de diretórios estruturada.

```bash
# Organizar por paciente (move arquivos)
python DICOM_reencoder/organize_dicom.py -s /origem -d /destino -m patient

# Organizar por série (copia, mantém originais)
python DICOM_reencoder/organize_dicom.py -s /origem -d /destino -m series --copy

# Organizar recursivamente
python DICOM_reencoder/organize_dicom.py -s /origem -d /destino -m study -r

# Organizar por modalidade
python DICOM_reencoder/organize_dicom.py -s /origem -d /destino -m modality
```

**Modos de Organização:**

| Modo | Estrutura de Diretórios |
|------|-------------------------|
| `patient` | `PatientName/PatientID/` |
| `study` | `PatientName/StudyDate_StudyDescription/` |
| `series` | `PatientName/StudyDate/SeriesNumber_SeriesDescription/` |
| `modality` | `Modality/PatientName/` |

**Opções:**
- `--copy`: Copia arquivos ao invés de mover
- `-r`: Busca recursiva na origem
- Sanitiza nomes de arquivos/pastas automaticamente
- Renomeia por Instance Number em modo series

---

### 🔍 Pesquisa e Filtragem

#### 12. `search_dicom.py` - Pesquisa por Critérios

Pesquisa arquivos DICOM baseado em critérios de metadados com suporte para wildcards e regex.

```bash
# Pesquisar por nome de paciente
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms --patient-name "Doe*"

# Pesquisar por modalidade
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms --modality CT

# Pesquisar por descrição de estudo (match parcial)
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms --study-desc "chest"

# Pesquisa customizada por tags
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms -t PatientID=12345 -t Modality=MR

# Pesquisa por intervalo de datas
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms --date-range 20240101 20241231

# Exportar resultados em CSV
python DICOM_reencoder/search_dicom.py -d /caminho/dicoms --modality CT --format csv
```

**Recursos:**
- **Wildcard matching:** `*` para padrões (ex: "Doe*")
- **Regex matching:** `/padrão/` para regex (ex: "/^CT.*/")
- **Busca recursiva:** `-r` flag
- **Formatos de saída:** table, list, csv
- **Critérios múltiplos:** Combina múltiplos filtros

**Campos de Pesquisa:**
- Patient Name, Patient ID
- Study Description, Study Date
- Modality
- Tags customizadas (-t)

---

### 🎞️ Multi-frame

#### 13. `split_multiframe.py` - Divisão de Multi-frame

Divide arquivos DICOM multi-frame em arquivos single-frame individuais.

```bash
# Dividir todos os frames
python DICOM_reencoder/split_multiframe.py multiframe.dcm

# Dividir para diretório específico
python DICOM_reencoder/split_multiframe.py multiframe.dcm -o ./saida

# Dividir com prefixo customizado
python DICOM_reencoder/split_multiframe.py multiframe.dcm --prefix ct_scan

# Extrair apenas frames específicos
python DICOM_reencoder/split_multiframe.py multiframe.dcm --frames 1 5 10 15

# Mostrar informações sem dividir
python DICOM_reencoder/split_multiframe.py multiframe.dcm --info
```

**Recursos:**
- Cria arquivos single-frame para cada frame
- Mantém metadados originais
- Gera novos SOP Instance UIDs
- Mantém mesmo Series Instance UID
- Numera arquivos por Instance Number
- Modo `--info` para pré-visualização
- Extração seletiva de frames específicos

---

### 📦 Processamento em Lote

#### 14. `batch_process.py` - Operações em Batch

Processa múltiplos arquivos DICOM de uma vez com várias operações.

```bash
# Listar todos os arquivos DICOM
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o list

# Listar recursivamente
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o list -r

# Descomprimir todos os arquivos
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o decompress

# Descomprimir para diretório específico
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o decompress --output-dir ./descomprimidos

# Anonimizar todos os arquivos
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o anonymize --output-dir ./anonimizados

# Converter todos para PNG
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o convert --format png --output-dir ./imagens

# Validar todos os arquivos
python DICOM_reencoder/batch_process.py -d /caminho/dicoms -o validate

# Com comandos CLI (após instalação)
dicom-batch -d /caminho/dicoms -o anonymize --output-dir ./anonimizados
```

**Operações Disponíveis:**
- `list` - Lista arquivos com informações básicas
- `decompress` - Descomprime arquivos
- `anonymize` - Anonimiza arquivos
- `convert` - Converte para PNG/JPEG
- `validate` - Valida arquivos

**Recursos:**
- Busca recursiva com `-r`
- Diretório de saída customizado
- Rastreamento de progresso
- Relatório de erros
- Suporta múltiplos formatos DICOM

---

### 🌐 DICOM Networking (NOVO!)

#### 15. `dicom_query.py` - Query PACS (C-FIND)

Pesquisa estudos em servidores PACS usando o protocolo DICOM C-FIND.

```bash
# Pesquisar estudos por nome de paciente
python DICOM_reencoder/dicom_query.py -H pacs.hospital.com -p 11112 --patient-name "Silva*"

# Ou usar comando CLI
dicom-query -H pacs.hospital.com -p 11112 --patient-name "Silva*"

# Pesquisar por modalidade
dicom-query -H pacs.hospital.com -p 11112 --modality CT

# Pesquisar por intervalo de datas
dicom-query -H pacs.hospital.com -p 11112 --study-date 20240101-20241231

# Pesquisar estudos com descrição específica
dicom-query -H pacs.hospital.com -p 11112 --study-desc "Chest"

# Pesquisar com AE titles customizados
dicom-query -H pacs.hospital.com -p 11112 --aet MYAE --aec PACSAE --patient-id 12345

# Pesquisar séries de um estudo
dicom-query -H pacs.hospital.com -p 11112 --level SERIES --study-uid 1.2.3.4.5

# Ativar debug logging
dicom-query -H pacs.hospital.com -p 11112 --patient-name "Silva*" --debug
```

**Níveis de Query:**
- `PATIENT` - Pesquisa pacientes
- `STUDY` - Pesquisa estudos (padrão)
- `SERIES` - Pesquisa séries (requer --study-uid)

**Critérios de Pesquisa:**
- Patient Name, Patient ID
- Study Date, Study Description
- Modality, Accession Number
- Suporte para wildcards (`*`)

**Formatos de Data:**
- Data única: `20240101`
- Intervalo: `20240101-20241231`
- Wildcards: `2024*`

---

#### 16. `dicom_retrieve.py` - Retrieve de PACS (C-MOVE/C-GET)

Busca estudos de servidores PACS usando C-MOVE ou C-GET.

```bash
# Buscar estudo usando C-GET (recomendado)
python DICOM_reencoder/dicom_retrieve.py -H pacs.hospital.com -p 11112 \
    --study-uid 1.2.3.4.5 -o ./estudos

# Ou usar comando CLI
dicom-retrieve -H pacs.hospital.com -p 11112 --study-uid 1.2.3.4.5 -o ./estudos

# Buscar série específica
dicom-retrieve -H pacs.hospital.com -p 11112 \
    --study-uid 1.2.3.4.5 --series-uid 1.2.3.4.6 -o ./series

# Buscar usando C-MOVE (envia para terceiro)
dicom-retrieve -H pacs.hospital.com -p 11112 \
    --study-uid 1.2.3.4.5 --use-move --move-dest MYAE

# Buscar com AE titles customizados
dicom-retrieve -H pacs.hospital.com -p 11112 \
    --aet WORKSTATION --aec PACSSERVER --study-uid 1.2.3.4.5 -o ./output

# Buscar instância específica
dicom-retrieve -H pacs.hospital.com -p 11112 \
    --study-uid 1.2.3.4.5 --series-uid 1.2.3.4.6 --instance-uid 1.2.3.4.7 -o ./images
```

**Protocolos:**
- **C-GET** (padrão) - Busca diretamente para esta aplicação
- **C-MOVE** - Envia para um AE Title de destino

**Níveis de Retrieve:**
- `STUDY` - Busca estudo completo
- `SERIES` - Busca série específica
- `IMAGE` - Busca instância específica

**Recursos:**
- Progressão em tempo real
- Salvamento automático de arquivos
- Suporte para múltiplos transfer syntaxes
- Logging detalhado

---

### 🖥️ Interface Web (NOVO!)

#### 17. `web_interface.py` - Servidor Web Flask

Interface web completa para visualização e processamento de DICOM files.

```bash
# Iniciar servidor web (porta padrão 5000)
python DICOM_reencoder/web_interface.py

# Ou usar comando CLI
dicom-web

# Iniciar em porta customizada
dicom-web -p 8080

# Permitir acesso externo (cuidado em produção!)
dicom-web -H 0.0.0.0 -p 8080

# Modo debug
dicom-web --debug
```

**Acesse:** http://localhost:5000

**Funcionalidades da Interface Web:**

1. **📤 Upload de Arquivos**
   - Drag & drop de arquivos DICOM
   - Validação automática
   - Visualização de informações básicas

2. **🖼️ Visualizador de Imagens**
   - Renderização de pixel data com windowing
   - Suporte para MONOCHROME1/MONOCHROME2
   - Visualização de multi-frame (primeiro frame)

3. **📊 Metadados**
   - Visualização de metadados completos
   - Organização por categorias
   - Patient, Study, Series, Image info

4. **📈 Estatísticas**
   - Estatísticas de pixel data
   - Min, Max, Mean, Median, Std Dev
   - Total de pixels e valores únicos

5. **🔒 Anonimização**
   - Anonimização com um clique
   - Download automático do arquivo anonimizado
   - Remoção de PHI completa

6. **✅ Validação**
   - Validação DICOM em tempo real
   - Exibição de erros e warnings
   - Verificação de conformidade

**API REST Endpoints:**

```
POST   /api/upload              - Upload de arquivo DICOM
GET    /api/metadata/<filename> - Obter metadados
GET    /api/image/<filename>    - Obter imagem PNG
GET    /api/stats/<filename>    - Estatísticas de pixels
POST   /api/anonymize/<filename>- Anonimizar arquivo
GET    /api/validate/<filename> - Validar arquivo
GET    /api/download/<filename> - Download de arquivo
```

**Recursos:**
- Interface responsiva e moderna
- Upload via drag & drop
- Preview de imagens em tempo real
- Processamento assíncrono
- CORS habilitado para integrações
- Limite de 100MB por arquivo

---

## Funcionalidades

### 📋 Extração de Metadados
- Exibição abrangente de metadados organizados por categoria
- Informações de Paciente, Estudo, Série, Imagem e Equipamento
- Detalhes de Transfer Syntax e Pixel Data
- Comparação entre arquivos

### 🔒 Anonimização
- Remoção HIPAA-compliant de PHI (Protected Health Information)
- Geração de IDs anônimos consistentes usando hashing
- Deslocamento de datas preservando relações temporais
- Regeneração de UIDs para privacidade
- Remoção de tags privadas de fabricantes

### 🔄 Conversão de Imagens
- Exportação para PNG ou JPEG
- Cálculo automático de windowing
- Suporte para tags DICOM Window/Level
- Processamento de multi-frame
- Suporte MONOCHROME1/MONOCHROME2

### ✅ Validação
- Verificação de conformidade DICOM
- Validação de tags obrigatórias (Type 1 e Type 2)
- Verificação de formato de UIDs
- Verificações de consistência de pixel data
- Validação de formato de datas/horários

### 📊 Análise de Pixel Data
- Estatísticas completas (min, max, mean, median, std, variance)
- Análise de percentis
- Histogramas visuais em texto
- Comparação entre arquivos
- Suporte para multi-frame

### ✏️ Modificação e Organização
- Modificação interativa ou batch de tags
- Organização automática por paciente/estudo/série/modalidade
- Sanitização de nomes de arquivos
- Modos copy ou move

### 🔍 Pesquisa Avançada
- Pesquisa por múltiplos critérios
- Suporte para wildcards e regex
- Pesquisa por intervalo de datas
- Múltiplos formatos de saída (table, list, csv)

### 🎞️ Multi-frame
- Divisão em single-frames
- Extração seletiva de frames
- Preservação de metadados
- Informações detalhadas de frames

### 📦 Processamento em Lote
- Múltiplas operações em batch
- Busca recursiva em diretórios
- Rastreamento de progresso e erros
- Operações: list, decompress, anonymize, convert, validate

---

## Estrutura do Repositório

```
Dicom-Tools/
├── DICOM_reencoder/                # Pacote Python principal
│   ├── __init__.py                 # Inicialização do módulo
│   ├── anonymize_dicom.py          # Anonimização HIPAA-compliant
│   ├── batch_process.py            # Processamento em lote
│   ├── comparar_dicom.py           # Comparação de metadados
│   ├── convert_to_image.py         # Conversão DICOM → PNG/JPEG
│   ├── decompress_dicom.py         # Descompressão de DICOM
│   ├── dicom_info.py               # Informações resumidas
│   ├── dicom_query.py              # ✨ Query PACS (C-FIND)
│   ├── dicom_retrieve.py           # ✨ Retrieve de PACS (C-MOVE/C-GET)
│   ├── extract_metadata.py         # Extração detalhada de metadados
│   ├── modify_tags.py              # Modificação de tags DICOM
│   ├── organize_dicom.py           # Organização estruturada
│   ├── pixel_stats.py              # Estatísticas de pixel data
│   ├── reencode_dicom.py           # Recodificação
│   ├── search_dicom.py             # Pesquisa por critérios
│   ├── split_multiframe.py         # Divisão de multi-frame
│   ├── validate_dicom.py           # Validação DICOM
│   ├── web_interface.py            # ✨ Interface Web Flask
│   └── web_templates/              # ✨ Templates HTML para web
│       └── index.html
│
├── setup.py                        # ✨ Setup para instalação pip
├── pyproject.toml                  # ✨ Configuração do projeto
├── requirements.txt                # ✨ Dependências Python
├── MANIFEST.in                     # ✨ Arquivos para distribuição
├── INSTALLATION.md                 # ✨ Guia de instalação detalhado
├── README.md                       # Documentação principal
└── LICENSE                         # Licença MIT
```

### 📦 Empacotamento

O projeto está completamente empacotado e pronto para distribuição via PyPI:

- **setup.py** - Script de instalação setuptools
- **pyproject.toml** - Configuração moderna de empacotamento
- **Entry points CLI** - 17 comandos globais após instalação
- **Módulo Python** - Importável como `import DICOM_reencoder`
- **Dependências gerenciadas** - requirements.txt e setup.py

---

## Próximos Passos

### ✅ Implementado v1.0.0
- [x] Empacotar utilitários como módulo Python ✨
- [x] Entry points CLI para todos os scripts ✨
- [x] Implementar DICOM query/retrieve (C-FIND, C-MOVE, C-GET) ✨
- [x] Interface web para visualização DICOM ✨
- [x] API REST para integração web ✨

### 🔄 Em Progresso / Futuro
- [ ] Adicionar testes automatizados com arquivos DICOM de amostra
- [ ] Publicar no PyPI para instalação via `pip install dicom-tools`
- [ ] Adicionar suporte para DICOM-RT (radioterapia)
- [ ] Criar script para combinar imagens em multi-frame
- [ ] Adicionar suporte para DICOM-SR (Structured Reports)
- [ ] Implementar DICOM SCP (Storage Service Class Provider)
- [ ] Adicionar suporte para DICOM Worklist (C-WORKLIST)
- [ ] Interface web: visualizador 3D para CT/MR
- [ ] Interface web: medições e anotações
- [ ] Dockerização da aplicação web
- [ ] Documentação API com Swagger/OpenAPI

---

## Licença

Este projeto está licenciado sob a Licença MIT. Veja [`LICENSE`](LICENSE) para detalhes.

---

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## Suporte

Para bugs, questões ou solicitações de features, por favor abra uma [issue](https://github.com/ThalesMMS/Dicom-Tools/issues).
