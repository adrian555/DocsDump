import os,shutil
rootDir="."
for dirName, subdirList, fileList in os.walk(rootDir):
  for sub in subdirList:
    t = os.path.join(dirName, sub)
    if not os.listdir(t):
      os.remove(t)
