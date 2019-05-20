# Install operator-sdk

[link](https://github.com/operator-framework/operator-sdk)

* Prereq:

```command line
apt-get update
apt-get install golang-go -y
mkdir -p /root/go/bin
export GOPATH=/root/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:.:$GOBIN
curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh
```

* Install:

```command line
mkdir -p $GOPATH/src/github.com/operator-framework
cd $GOPATH/src/github.com/operator-framework
git clone https://github.com/operator-framework/operator-sdk
cd operator-sdk
git checkout master
make dep
make install
```

