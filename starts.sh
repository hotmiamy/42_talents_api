#!/bin/bash

# Aplica migrações do banco
flask db upgrade

# Inicia o servidor
exec gunicorn --bind 0.0.0.0:$PORT app.app:app