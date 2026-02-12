# coleta_info_kv.ps1

# 1. Correção de Encoding (Crucial para acentos do ipconfig e nomes de usuário)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$destino = "P:\TI"

# 2. Valida diretório
if (-not (Test-Path $destino)) {
    Write-Host "ERRO: O diretório '$destino' não existe." -ForegroundColor Red
    exit 1
}

# 3. Pede nome
$nome = Read-Host "Nome do arquivo (ex: PC-JOAO)"
$nome = $nome.Trim()
if ([string]::IsNullOrWhiteSpace($nome)) { exit 1 }

# 4. Define arquivo
#$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$arquivo = Join-Path $destino ("{0}.txt" -f $nome)

Write-Host "Coletando dados..." -ForegroundColor Cyan

# 5. Coleta WMI/CIM
$comp = Get-CimInstance Win32_ComputerSystem
$os   = Get-CimInstance Win32_OperatingSystem
$proc = Get-CimInstance Win32_Processor

# Cálculos
$ramTotal = [math]::Round($comp.TotalPhysicalMemory / 1GB, 2)

# 6. Monta conteúdo no formato Chave: Valor
$linhas = @()

# Cabeçalho simples
$linhas += "Data_Geracao: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
$linhas += "Arquivo_Destino: $arquivo"
$linhas += ""

# Itens 1 a 6
$linhas += "Hostname: $($comp.Name)"
$linhas += "Sistema_Operacional: $($os.Caption)"
$linhas += "Modelo_Sistema: $($comp.Model)"
$linhas += "Memoria_Total_GB: $ramTotal"
$linhas += "Processador: $($proc.Name)"

# Item 7 - Discos (Loop para manter formato Chave:Valor)
$discos = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
foreach ($d in $discos) {
    $t = [math]::Round($d.Size/1GB, 2)
    $l = [math]::Round($d.FreeSpace/1GB, 2)
    # Formato: "Disco_C: Total 100GB, Livre 50GB"
    $linhas += "Disco_$($d.DeviceID.Replace(':','')): Total ${t} GB, Livre ${l} GB"
}

$linhas += ""
$linhas += "---- IPCONFIG_ALL_ABAIXO ----"
# Item 8 - IPConfig (Mantido bruto pois é um bloco complexo, mas limpo de erros de encoding)
$linhas += (ipconfig /all | Out-String).Trim()

# 7. Salva com Encoding UTF8
$linhas | Out-File -FilePath $arquivo -Encoding UTF8

Write-Host "Arquivo gerado: $arquivo" -ForegroundColor Green