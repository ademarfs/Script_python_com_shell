📊 Extrator de Informações de Servidores (Sysinfo to Excel)
Este script em Python automatiza a leitura de múltiplos arquivos de log (formato .txt), extrai informações essenciais de hardware e sistema operacional, e consolida tudo em uma planilha Excel (.xlsx) organizada.

🚀 Funcionalidades
Varredura Automática: Itera sobre todos os arquivos .txt de um diretório especificado.

Extração Inteligente: Busca por chaves flexíveis (ex: "Hostname", "Memória", "Disco") ignorando diferenças de maiúsculas/minúsculas.

Tratamento de Dados:

Converte automaticamente memória RAM de MB para GB.

Limpa caminhos de arquivos (remove prefixos como P:\TI\ e extensões).

Remove espaços e caracteres indesejados (\t, quebras de linha).

Exportação Excel: Gera um relatório final (Relatorio_Sysinfo.xlsx) com colunas ordenadas.

📋 Pré-requisitos
Certifique-se de ter o Python 3.x instalado. Além disso, você precisará das bibliotecas para manipulação de dados e criação de planilhas.

Instale as dependências executando:

Bash
pip install pandas openpyxl
⚙️ Configuração
Antes de rodar o script, é necessário ajustar o caminho da pasta onde estão os seus arquivos de texto.

Abra o arquivo do script (.py).

Localize a linha 5, onde está a variável DIRETORIO.

Altere o caminho para a pasta correta no seu computador:

Python
# Exemplo:
DIRETORIO = r'C:\Caminho\Para\Seus\Arquivos_TXT'
Nota: Mantenha o r antes das aspas para evitar erros com as barras invertidas do Windows.

📂 Estrutura dos Arquivos de Entrada
O script espera arquivos .txt que contenham informações no formato Chave: Valor ou Chave= Valor.

Campos extraídos:

Arquivo_Destino

Hostname

Sistema_Operacional

Modelo_Sistema

Memoria_Total_GB (Procura por "Memoria Total", "Total Physical Memory", etc.)

Processador

Disco_C e Disco_D

▶️ Como Executar
Abra o terminal ou CMD.

Navegue até a pasta onde o script está salvo.

Execute o comando:

Bash
python nome_do_seu_script.py
📤 Resultado
Após a execução, um arquivo chamado Relatorio_Sysinfo.xlsx será criado no mesmo diretório do script.

A tabela gerada seguirá esta ordem de colunas: | Arquivo_Destino | Hostname | Sistema_Operacional | Modelo_Sistema | Memoria_Total_GB | Processador | Disco_C | Disco_D | |-----------------|----------|---------------------|----------------|------------------|-------------|---------|---------|

🛠 Personalização (Opcional)
Se precisar adicionar novos campos de busca, edite o dicionário mapa_busca dentro da função processar_diretorio:

Python
mapa_busca = {
    # ... campos existentes ...
    "Nova_Coluna": ["palavra chave 1", "palavra chave 2"]
}

Notas: 
1. Faça os ajustes de diretório, tanto no "sysinfo_custom.ps1" quanto no "main.py";
2. Abrir o PowerShell;
3. Rodar o comando "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" para liberar o uso do script;
4. Rode o script "sysinfo_custom.ps1" acessando o diretorio raiz e chame-o com ".\sysinfo_custom.ps1";
5. Será gerado um .txt no diretório raiz;
6. Rode o script "main.py" e gere o arquivo Excel na raiz do projeto Python;