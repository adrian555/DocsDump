# Windows 10 Tips

* to access the files on the WSL2, using `\\wsl$` as the root path. VSCode can open the folder in WSL2.

* to mount usb drives, run

  ```shell
  mkdir /mnt/f
  mount -t drvfs f: /mnt/f
  ```

* from Windows PowerShell to access the dir in wsl

  ```shell
  cd "\\wsl$\Ubuntu-20.04\home\wzhuang"
  ```

* list all files and folders in a directory from PowerShell

  ```shell
  Get-ChildItem -Path . -Force
  ```

turn wake timers off
```shell
powercfg /SETACVALUEINDEX SCHEME_CURRENT 238c9fa8-0aad-41ed-83f4-97be242c8f20 bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d 0
powercfg /SETDCVALUEINDEX SCHEME_CURRENT 238c9fa8-0aad-41ed-83f4-97be242c8f20 bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d 0
```

disable maintanence activator- https://superuser.com/questions/1131231/how-do-i-prevent-the-windows-10-maintenance-activator-from-waking-my-pc-random

1. Ubuntu
2. VScode
3. Picasa
4. HRBlock
5. DiskStation
6. Thunderbird
7. Webpage to app: IB, Google Keep
8. Zoom
9. Powershell
10. Slack
11. Brother
12. Moneyspire
13. Freemake
14. Adobe Reader
15. LibreOffice
16. McAfee total protection
17. Python3.9
18. VLCplayer
19. Chinese
