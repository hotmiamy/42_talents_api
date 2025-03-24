#!/bin/bash

# Aplica migrações do banco
flask db upgrade

# Inicia o servidor
exec gunicorn --bind 0.0.0.0:5000 app.app:app