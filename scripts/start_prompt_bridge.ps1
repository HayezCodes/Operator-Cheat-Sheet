$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $repoRoot "bridge.config.json"

if (-not (Test-Path -LiteralPath $configPath)) {
    throw "Missing config file: $configPath"
}

$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$pollSeconds = [int]$config.poll_seconds
$autoOpenVsCode = [bool]$config.auto_open_vscode
$autoOpenPromptFile = [bool]$config.auto_open_prompt_file
$copyToClipboard = [bool]$config.copy_to_clipboard
$promptFolder = Join-Path $repoRoot $config.prompt_folder

if (-not (Test-Path -LiteralPath $promptFolder)) {
    New-Item -ItemType Directory -Path $promptFolder -Force | Out-Null
}

$codeCommand = Get-Command code -ErrorAction SilentlyContinue
$openedRepoInCode = $false
$lastPromptSignature = $null

function Open-RepoInVsCode {
    param(
        [string]$RepoPath
    )

    if (-not $script:autoOpenVsCode) {
        return
    }

    if (-not $script:codeCommand) {
        Write-Warning "VS Code command 'code' was not found on PATH."
        return
    }

    if (-not $script:openedRepoInCode) {
        & $script:codeCommand.Path $RepoPath | Out-Null
        $script:openedRepoInCode = $true
    }
}

function Open-PromptFileInVsCode {
    param(
        [string]$FilePath
    )

    if (-not $script:autoOpenPromptFile) {
        return
    }

    if (-not $script:codeCommand) {
        Write-Warning "VS Code command 'code' was not found on PATH."
        return
    }

    & $script:codeCommand.Path -g $FilePath | Out-Null
}

function Get-NewestPromptFile {
    param(
        [string]$FolderPath
    )

    $files = Get-ChildItem -LiteralPath $FolderPath -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -in @(".md", ".txt") } |
        Sort-Object LastWriteTimeUtc -Descending

    return $files | Select-Object -First 1
}

function Get-PromptSignature {
    param(
        [System.IO.FileInfo]$File
    )

    return "{0}|{1}" -f $File.FullName, $File.LastWriteTimeUtc.Ticks
}

function Print-And-HandlePrompt {
    param(
        [System.IO.FileInfo]$PromptFile
    )

    $content = Get-Content -LiteralPath $PromptFile.FullName -Raw

    Write-Host ""
    Write-Host ("=" * 80)
    Write-Host ("Newest prompt: {0}" -f $PromptFile.FullName)
    Write-Host ("Updated: {0}" -f $PromptFile.LastWriteTime)
    Write-Host ("=" * 80)
    Write-Host $content
    Write-Host ("=" * 80)

    if ($script:copyToClipboard) {
        try {
            Set-Clipboard -Value $content
            Write-Host "Prompt copied to clipboard."
        }
        catch {
            Write-Warning ("Failed to copy prompt to clipboard: {0}" -f $_.Exception.Message)
        }
    }

    Open-RepoInVsCode -RepoPath $script:repoRoot
    Open-PromptFileInVsCode -FilePath $PromptFile.FullName
}

Write-Host ("Prompt bridge started in {0}" -f $repoRoot)
Write-Host ("Watching folder: {0}" -f $promptFolder)
Write-Host ("Polling every {0} seconds" -f $pollSeconds)

Open-RepoInVsCode -RepoPath $repoRoot

while ($true) {
    try {
        Write-Host ""
        Write-Host ("[{0}] Running git pull..." -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
        & git -C $repoRoot pull

        $latestPrompt = Get-NewestPromptFile -FolderPath $promptFolder

        if ($null -eq $latestPrompt) {
            Write-Host "No prompt files found."
        }
        else {
            $currentSignature = Get-PromptSignature -File $latestPrompt

            if ($currentSignature -ne $lastPromptSignature) {
                Print-And-HandlePrompt -PromptFile $latestPrompt
                $lastPromptSignature = $currentSignature
            }
            else {
                Write-Host ("No new prompt since last handled file: {0}" -f $latestPrompt.Name)
            }
        }
    }
    catch {
        Write-Warning ("Bridge loop error: {0}" -f $_.Exception.Message)
    }

    Start-Sleep -Seconds $pollSeconds
}
