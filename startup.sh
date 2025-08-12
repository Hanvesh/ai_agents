#!/bin/bash


# ELK Logs
gunicorn --config gunicorn_config.py start:app
