#!/bin/bash

pytest Functionality/Compiled Performance/Compiled Security/Compiled Usability/Compiled -v

# Execution of Security Related Tasks that is not dependent to pytest.
python3 Security/Compiled/BruteForceLogin.py

python3 Security/Compiled/CipherEnum.py

python3 Security/Compiled/SessionManagement.py
