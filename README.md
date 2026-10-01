# pcnotify ahora es PendiFy

El programa cambió de nombre y se mudó a https://github.com/ElkinDev/PendiFy.

Para instalar PendiFy, pulsa Windows + R, pega esta línea completa y pulsa Enter:

    powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pendify-install.ps1 -ea 0; irm https://raw.githubusercontent.com/ElkinDev/PendiFy/main/install.ps1 -OutFile ~\pendify-install.ps1; ~\pendify-install.ps1"

Si este PC tiene pcnotify:

1. Quítalo primero con la línea de desinstalación de este repositorio, pegada igual que la de instalación:

       powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pcnotify-uninstall.ps1 -ea 0; irm https://raw.githubusercontent.com/ElkinDev/pcnotify/main/uninstall.ps1 -OutFile ~\pcnotify-uninstall.ps1; ~\pcnotify-uninstall.ps1"

2. Instala PendiFy con la línea de arriba.
3. Enlaza el PC otra vez desde la página de PendiFy: el enlace de pcnotify no pasa a PendiFy.

# pcnotify is now PendiFy

The program changed its name and moved to https://github.com/ElkinDev/PendiFy.

To install PendiFy, press Windows + R, paste this whole line and press Enter:

    powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pendify-install.ps1 -ea 0; irm https://raw.githubusercontent.com/ElkinDev/PendiFy/main/install.ps1 -OutFile ~\pendify-install.ps1; ~\pendify-install.ps1"

If this PC has pcnotify:

1. Remove it first with this repository's uninstall line, pasted the same way as the install line:

       powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pcnotify-uninstall.ps1 -ea 0; irm https://raw.githubusercontent.com/ElkinDev/pcnotify/main/uninstall.ps1 -OutFile ~\pcnotify-uninstall.ps1; ~\pcnotify-uninstall.ps1"

2. Install PendiFy with the line above.
3. Link the PC again from PendiFy's page: the pcnotify link is not carried over to PendiFy.
