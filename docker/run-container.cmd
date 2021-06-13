:: This bat will add a container
:: specify container name = %1

@echo off

cd ../

IF "%~1" == "" GOTO NoName
echo run ubuntu18.04...
docker run -v "%cd%":/ai --name %1 -it ubuntu18.04

:NoName
docker run -v "%cd%":/ai -it ubuntu18.04
