# pcnotify is now PendiFy. This file installs nothing any more: it only prints where the program
# moved and the PendiFy install line, and leaves exit code 1. It reads no environment variable,
# looks for no Python, creates nothing and fetches nothing.
# It runs as a file and as text piped into PowerShell, so it takes no parameters.
# The file is pure ASCII: Windows PowerShell 5.1 reads a file with no byte order mark in the
# system code page, so the messages are Spanish written without accented letters.

& {
    $NewLine = 'powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pendify-install.ps1 -ea 0; irm https://raw.githubusercontent.com/ElkinDev/PendiFy/main/install.ps1 -OutFile ~\pendify-install.ps1; ~\pendify-install.ps1"'

    function Invoke-Notice {
        Write-Host 'pcnotify ahora es PendiFy: https://github.com/ElkinDev/PendiFy'
        Write-Host 'Esta linea ya no instala nada. Para instalar PendiFy, pega esta linea:'
        Write-Host $NewLine
        Write-Host ''
        Write-Host 'pcnotify is now PendiFy: https://github.com/ElkinDev/PendiFy'
        Write-Host 'This line installs nothing any more. To install PendiFy, paste this line:'
        Write-Host $NewLine
        return 1
    }

    $code = Invoke-Notice
    # As a file the exit code is the process's; piped, exit would close the person's window, so the
    # code is left in LASTEXITCODE instead.
    if ($PSCommandPath) { exit $code }
    $global:LASTEXITCODE = $code
}
