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
