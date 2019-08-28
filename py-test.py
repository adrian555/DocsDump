import sys
def run(input):
  print(input)
  return(input)

def check_call(f, args):
  print("check_call")
  res = f(args)
  if res > 0:
    sys.exit(res)

if __name__ == "__main__":
  check_call(run, 0)
  check_call(run, 1)
  check_call(run, 0)