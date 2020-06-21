#!/bin/bash
pwd

if [ "$1" == "" ]; then
	echo "Enter the directory where blender 2.8X is installed"
else
	echo "$1"
	cd $1
	cd 2.8*
	cd python/bin
	wget https://bootstrap.pypa.io/get-pip.py
	ls
	./python3.* get-pip.py
	ls
	./pip3 install ase
fi
