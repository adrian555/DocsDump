* To fully bring down an OKD cluster:

```command line
oc cluster down
df |grep openshift|awk '{print $6}' |while read line; do umount $line; done
rm -rf /var/lib/origin
```