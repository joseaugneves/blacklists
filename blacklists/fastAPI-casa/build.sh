. app.env
if [ "$ISLATEST" = "true" ] ; then
  echo "tagging $IMAGENAME:$IMAGETAG $IMAGENAME:latest"
  docker build --build-arg BASEIMAGE=$BASEIMAGE -t $IMAGENAME:$IMAGETAG -t $IMAGENAME:latest .
else
  echo "tagging $IMAGENAME:$IMAGETAG"
  docker build --build-arg BASEIMAGE=$BASEIMAGE -t $IMAGENAME:$IMAGETAG .
fi
