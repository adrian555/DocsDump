import os,shutil,sys
rootDir="."
dst=sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(rootDir))
dstDir=os.path.join(dst, "photo-to-import")
numMove=0
numNo=0
if not os.path.exists(dstDir):
  os.makedirs(dstDir)
for dirName, subdirList, fileList in os.walk(rootDir):
  for fname in fileList:
    t=os.path.join(dstDir, fname)
    if not os.path.exists(t):
      numMove=numMove+1
      shutil.move(os.path.join(dirName,fname), os.path.join(dstDir,fname))
    else:
      numNo=numNo+1
      print(os.path.join(dirName, fname))
print(numMove, numNo)
