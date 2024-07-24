#!/usr/bin/bash

# This script is a wrapper for a python script run in docker

#BASE_DIR="$HOME/.aisuggestions"
BASE_DIR="$HOME/vscode/aicodesuggestion"
CONFIG_DIR="$HOME/.aicodesuggestions"
IMAGENAME="aicodesuggestions"



# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
    #die "Base directory $BASE_DIR does not exist"
    echo "Base directory $BASE_DIR does not exist"
    exit 1
fi

# Check if the config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir "$CONFIG_DIR"
fi




#####check to see if we need to rebuild the container
#using perl instead of stat  becaues it works the same on linux and mac
VERSION=$(perl -e "open(\$fh, '${BASE_DIR}/Dockerfile'); @stats = stat(\$fh); print \$stats[9];")

#echo "Version: $VERSION"
CURRENTVERSION=`docker images | grep "$IMAGENAME" | awk  '{print $2}'`

if [ "$VERSION" != "$CURRENTVERSION" ]; then
        if [ -z "$CURRENTVERSION" ]; then
                echo "no image built, building"
        else
                echo "wrong version of image build, removing and rebuilding"
                imageid=`docker images | grep $IMAGENAME | awk  '{print $3}'`
                echo "remove image $imageid"
                docker rmi -f $imageid
        fi
        #echo "building image $IMAGENAME:$VERSION"
        docker build -t $IMAGENAME:$VERSION $BASE_DIR/
fi



#uses copy instead of mount:
#echo "running image $IMAGENAME:$VERSION"
#docker run -it --rm -v "$CONFIG_DIR/config.json:/app/config.json" -v "$(pwd):/app/data" $IMAGENAME:$VERSION python aicodesuggestions.py "$@"

# ...

# Define the code directory (you can modify this to point to the actual code directory)
CODE_DIR="$BASE_DIR/code"

#echo "running image $IMAGENAME:$VERSION"
docker run -it --rm -v "$CONFIG_DIR/config.json:/app/config.json" -v "$CODE_DIR:/usr/src/app" -v "$(pwd):/app/data" $IMAGENAME:$VERSION python aicodesuggestions.py "$@"
