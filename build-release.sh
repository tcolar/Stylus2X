#!/bin/sh
echo "release version?"
read release
folder="stylus2x-$release"
mkdir "$folder"
cp README.txt src/*.py src/*.gpe src/*.png src/*.ttf $folder
mkdir dist
tar czvf "dist/$folder.tgz" "$folder"
rm -rf "$folder"
echo "built dist/$folder.tgz"
