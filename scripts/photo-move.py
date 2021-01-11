import os,shutil
rootDir="."
dstDir=os.path.dirname(os.path.abspath(rootDir))
for dirName, subdirList, fileList in os.walk(rootDir):
  for fname in fileList:
    x=fname.split(".")
    if len(x) > 1:
      if x[1] == 'jpg' or x[1] == 'mp4':
        print(x[0])
        y=x[0].split("_")
        if len(y) > 1:
          year=y[0][0:4]
          month=y[0][4:6]
          day=y[0][6:8]
          # t=os.path.join(dirName, year+"-"+month+"-"+day)
          t=os.path.join(dstDir, year+"-"+month+"-"+day)
          if not os.path.exists(t):
            os.makedirs(t)
          shutil.move(os.path.join(dirName,fname), os.path.join(t,fname))
