#!/usr/bin/env bash
# CPU жүктемесін жасанды түрде арттыру (шексіз цикл ~1 ядро алады)
kubectl run load-generator --image=busybox:1.36 --restart=Never -n default -- /bin/sh -c "while true; do :; done"
