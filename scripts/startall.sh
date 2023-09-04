#!/bin/bash
echo "==========================="
echo "=      STARTING ORDS      ="
echo "==========================="

ords/bin/ords serve &

echo "==========================="
echo "=  STARTING JUPYTER-LAB   ="
echo "==========================="

jupyter-lab --allow-root --ip 0.0.0.0 --port 8888 --no-browser
