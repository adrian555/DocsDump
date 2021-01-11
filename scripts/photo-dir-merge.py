import os,shutil,sys
srcDir = "."
dstDir = sys.argv[1]
num = 0
for dirName, subdirList, fileList in os.walk(srcDir):
  for sub in subdirList:
    dstSub = os.path.join(dstDir, sub)
    srcSub = os.path.join(dirName, sub)
    if not os.path.exists(dstSub):
      os.makedirs(dstSub)
    for f in os.listdir(srcSub):
      if not os.path.exists(os.path.join(dstSub, f)):
        print(num, os.path.join(srcSub, f))
        shutil.move(os.path.join(srcSub, f), os.path.join(dstSub, f))
        num = num + 1
