import os
import pandas as pd
import re

DIRETORIO = r'C:\Users\adema\OneDrive\Desktop\test txt'

def limpar_valor(texto):
    """Remove caracteres indesejados e espaços extras."""
    if not texto: return None
    return texto.strip().replace('\t', '')

def extrair_dado(linha, chaves_possiveis):
    """Verifica e extrai valor da linha baseado nas chaves."""
    linha_lower = linha.lower()
    for chave in chaves_possiveis:
        if chave.lower() in linha_lower:
            if ':' in linha:
                return limpar_valor(linha.split(':', 1)[1])
            elif '=' in linha:
                return limpar_valor(linha.split('=', 1)[1])
    return None

def processar_diretorio(diretorio_alvo):
    dados_servidores = []
    
    # 1. Mapeamento Atualizado
    mapa_busca = {
        "Arquivo_Destino":      ["Arquivo_Destino"],
        "Hostname":             ["Hostname"],
        "Sistema_Operacional":  ["Sistema_Operacional"],
        "Modelo_Sistema":       ["Modelo_Sistema"],
        "Memoria_Total_GB":     ["Memoria_Total_GB"],
        "Processador":          ["Processador"],
        "Disco_C":              ["Disco_C"],
        "Disco_D":              ["Disco_D"]
    }

    arquivos_txt = [f for f in os.listdir(diretorio_alvo) if f.endswith(".txt") and "_att" not in f and "requirements" not in f]
    print(f"Processando {len(arquivos_txt)} arquivos...\n")

    for arquivo in arquivos_txt:
        caminho_completo = os.path.join(diretorio_alvo, arquivo)
        
        # Inicializa dicionário vazio
        info_servidor = {k: None for k in mapa_busca.keys()}
        
        try:
            # Tenta ler o arquivo (UTF-8 ou Latin-1)
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
            except UnicodeDecodeError:
                with open(caminho_completo, 'r', encoding='latin-1') as f:
                    linhas = f.readlines()

            # Extração dos dados
            for linha in linhas:
                linha_limpa = linha.strip()
                if not linha_limpa: continue

                for campo, chaves in mapa_busca.items():
                    if info_servidor[campo] is None:
                        valor = extrair_dado(linha_limpa, chaves)
                        if valor:
                            info_servidor[campo] = valor

            # --- ZONA DE TRATAMENTO DE DADOS ---

            # 1. Tratamento Específico: Arquivo_Destino
            # Transforma "P:\TI\ti.txt" em "ti"
            destino = info_servidor["Arquivo_Destino"]
            if destino:
                # Remove o caminho fixo (Note as duas barras invertidas \\ para escapar no Python)
                destino = destino.replace("P:\\TI\\", "")
                # Remove a extensão
                destino = destino.replace(".txt", "")
                # Atualiza o valor limpo no dicionário
                info_servidor["Arquivo_Destino"] = destino.strip()

            # 2. Tratamento Específico: Memória (MB para GB)
            mem = info_servidor["Memoria_Total_GB"]
            if mem and "MB" in mem.upper():
                try:
                    numeros = re.findall(r"[\d\.,]+", mem)
                    if numeros:
                        val = numeros[0].replace('.', '').replace(',', '.')
                        gb = float(val) / 1024
                        info_servidor["Memoria_Total_GB"] = round(gb, 2)
                except:
                    pass 

            dados_servidores.append(info_servidor)

        except Exception as e:
            print(f"[ERRO] {arquivo}: {e}")

    # Geração do Excel
    if dados_servidores:
        df = pd.DataFrame(dados_servidores)
        
        # Ordenação das colunas conforme pedido
        colunas_ordem = ["Arquivo_Destino", "Hostname", "Sistema_Operacional", "Modelo_Sistema", 
                         "Memoria_Total_GB", "Processador", "Disco_C", "Disco_D"]
        
        # Garante que todas colunas existam, mesmo se vierem vazias
        df = df.reindex(columns=colunas_ordem)

        nome_excel = "Relatorio_Sysinfo.xlsx"
        df.to_excel(nome_excel, index=False)
        
        print("\n" + "="*40)
        print(f"SUCESSO! Arquivo gerado: {nome_excel}")
        print("="*40)
        print(df[["Arquivo_Destino", "Hostname"]].head().to_string()) # Mostra prévia
    else:
        print("Nenhum dado encontrado.")

if __name__ == "__main__":
    processar_diretorio(DIRETORIO)