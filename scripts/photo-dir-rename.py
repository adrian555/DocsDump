import os,shutil
rootDir="."
for dirName, subdirList, fileList in os.walk(rootDir):
  for dir in subdirList:
    x=dir.split("_")
    if len(x) > 1:
      t=x[0]
      for i in range(1, len(x)):
        t=t+"-"+x[i]
      print(t)
      shutil.move(os.path.join(dirName,dir), os.path.join(dirName,t))
