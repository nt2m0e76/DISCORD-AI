@echo off
start cmd /k "python ollama_server.py"
timeout /t 3
start cmd /k "python bot.py"