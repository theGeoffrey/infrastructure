#!/bin/bash

set -e
export branch="deploy-$(date +%s)"
export current=`git rev-parse HEAD`

git checkout -b $branch
npm install
mv geoffrey/ui/dist ui-dist
git add -f ui-dist/* promo/dist/*
git commit -m"Add compiled UIs for deploy"
git push deploy $branch:master
git tag -f deployed $current
git push origin --tags