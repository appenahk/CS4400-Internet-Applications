#!/bin/bash

IP=$(hostname - I)
python servertest.py $IP $1


