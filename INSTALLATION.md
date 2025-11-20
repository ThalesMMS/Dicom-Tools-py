# Guia de Instalação - DICOM Tools

## Métodos de Instalação

### 1. Instalação via pip (Recomendado)

```bash
# Instalar diretamente do repositório
pip install git+https://github.com/ThalesMMS/Dicom-Tools.git

# Ou instalar do diretório local
pip install .

# Instalar em modo desenvolvimento (editable)
pip install -e .
```

### 2. Instalação Manual

```bash
# Clonar o repositório
git clone https://github.com/ThalesMMS/Dicom-Tools.git
cd Dicom-Tools

# Criar ambiente virtual (recomendado)
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# OU
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar o pacote
pip install -e .
```

### 3. Instalação com Funcionalidades Opcionais

```bash
# Instalar com ferramentas de desenvolvimento
pip install -e ".[dev]"

# Instalar apenas componentes web
pip install -e ".[web]"

# Instalar apenas componentes de networking
pip install -e ".[networking]"

# Instalar tudo
pip install -e ".[dev,web,networking]"
```

## Verificação da Instalação

### Verificar comandos CLI instalados

```bash
# Listar todos os comandos disponíveis
dicom-info --help
dicom-query --help
dicom-web --help

# Testar extração de metadados
dicom-extract-metadata seu_arquivo.dcm

# Iniciar interface web
dicom-web
```

### Verificar importação do módulo Python

```python
import DICOM_reencoder
print(DICOM_reencoder.__version__)

# Usar funções programaticamente
from DICOM_reencoder import anonymize_dicom
anonymize_dicom.anonymize_dicom('input.dcm', 'output.dcm')
```

## Comandos CLI Disponíveis

Após a instalação, os seguintes comandos estarão disponíveis globalmente:

### Inspeção e Metadados
- `dicom-extract-metadata` - Extrai metadados detalhados
- `dicom-info` - Informações resumidas
- `dicom-compare` - Compara dois arquivos

### Conversão
- `dicom-reencode` - Recodifica transfer syntax
- `dicom-decompress` - Descomprime DICOM
- `dicom-to-image` - Converte para PNG/JPEG

### Privacidade
- `dicom-anonymize` - Anonimiza arquivos

### Validação
- `dicom-validate` - Valida conformidade
- `dicom-pixel-stats` - Estatísticas de pixels

### Modificação
- `dicom-modify` - Modifica tags
- `dicom-organize` - Organiza arquivos

### Pesquisa
- `dicom-search` - Pesquisa por critérios

### Multi-frame
- `dicom-split-multiframe` - Divide multi-frame

### Batch
- `dicom-batch` - Processamento em lote

### Networking (NOVO!)
- `dicom-query` - C-FIND para PACS
- `dicom-retrieve` - C-MOVE/C-GET de PACS

### Web Interface (NOVO!)
- `dicom-web` - Inicia servidor web

## Exemplos de Uso Rápido

### Interface Web
```bash
# Iniciar servidor web na porta padrão (5000)
dicom-web

# Iniciar em porta customizada
dicom-web -p 8080

# Permitir acesso externo
dicom-web -H 0.0.0.0 -p 8080
```

Acesse: http://localhost:5000

### Query PACS
```bash
# Pesquisar estudos por paciente
dicom-query -H pacs.hospital.com -p 11112 --patient-name "Silva*"

# Pesquisar por modalidade
dicom-query -H pacs.hospital.com -p 11112 --modality CT

# Pesquisar por intervalo de datas
dicom-query -H pacs.hospital.com -p 11112 --study-date 20240101-20241231
```

### Retrieve de PACS
```bash
# Buscar estudo usando C-GET
dicom-retrieve -H pacs.hospital.com -p 11112 --study-uid 1.2.3.4.5 -o ./estudos

# Buscar usando C-MOVE
dicom-retrieve -H pacs.hospital.com -p 11112 --study-uid 1.2.3.4.5 --use-move --move-dest MYAE
```

### Processamento em Batch
```bash
# Anonimizar todos os arquivos de um diretório
dicom-batch -d /path/dicoms -o anonymize --output-dir ./anonimizados

# Validar todos os arquivos
dicom-batch -d /path/dicoms -o validate
```

## Dependências

### Obrigatórias
- Python >= 3.9
- pydicom >= 2.3.0
- numpy >= 1.20.0
- Pillow >= 9.0.0
- pynetdicom >= 2.0.0 (para networking)
- flask >= 2.0.0 (para web interface)
- flask-cors >= 3.0.0

### Opcionais (Desenvolvimento)
- pytest >= 7.0.0
- pytest-cov >= 3.0.0
- black >= 22.0.0
- flake8 >= 4.0.0

## Solução de Problemas

### Erro: Comando não encontrado
Se os comandos CLI não estiverem disponíveis após a instalação:

```bash
# Reinstalar com pip
pip install --force-reinstall .

# Verificar se os scripts estão no PATH
which dicom-info  # Linux/Mac
where dicom-info  # Windows
```

### Erro de Importação
Se encontrar erros de importação:

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar instalação do pydicom
python -c "import pydicom; print(pydicom.__version__)"
```

### Problemas com pynetdicom
Para recursos de networking (C-FIND, C-MOVE):

```bash
# Instalar/atualizar pynetdicom
pip install --upgrade pynetdicom
```

### Problemas com Interface Web
Se a interface web não iniciar:

```bash
# Instalar dependências web
pip install flask flask-cors

# Verificar porta disponível
dicom-web -p 8080  # Tentar outra porta
```

## Desinstalação

```bash
# Desinstalar o pacote
pip uninstall dicom-tools

# Remover ambiente virtual (se usado)
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows
```

## Atualização

```bash
# Atualizar do repositório
pip install --upgrade git+https://github.com/ThalesMMS/Dicom-Tools.git

# Atualizar instalação local
git pull
pip install --upgrade .
```

## Configuração Avançada

### Variáveis de Ambiente

```bash
# Diretório temporário para uploads web
export DICOM_WEB_UPLOAD_DIR=/tmp/dicom_uploads

# Tamanho máximo de arquivo (bytes)
export DICOM_WEB_MAX_SIZE=104857600  # 100MB
```

### Configuração do PACS

Para usar query/retrieve, você pode criar um arquivo de configuração:

```bash
# ~/.dicom-tools/pacs.conf
[DEFAULT]
host = pacs.hospital.com
port = 11112
aet = DICOM_TOOLS
aec = PACS_SERVER
```

## Suporte

Para problemas ou dúvidas:
- Issues: https://github.com/ThalesMMS/Dicom-Tools/issues
- Documentação: https://github.com/ThalesMMS/Dicom-Tools#readme
