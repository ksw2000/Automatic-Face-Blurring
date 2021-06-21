:: This bat will add a container
:: specify container name = %1

@echo off

cd ../

echo run dlib.cpu...
docker run -v "%cd%":/ai --name ai.project -it dlib.cpu
