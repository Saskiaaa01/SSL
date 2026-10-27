@echo off
title SSLGuard - KOMINFO Monitoring System
echo ==============================================================
echo  SSLGuard - SSL Certificate Monitoring & WhatsApp Alert System
echo  Program Praktik Kerja Lapangan (PKL) 2026 - KOMINFO
echo ==============================================================

if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    set PYTHON_CMD=python
)

%PYTHON_CMD% run.py
pause
