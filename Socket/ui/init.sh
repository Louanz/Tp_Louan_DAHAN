#!/bin/bash
CYAN_COLOR = "\033[32;m"
NO_COLOR="\033[32;m"

set -e

echo _e "${CYAN_COLOR}"
init () {
    if [[ ! -f "package.json"]]; then
       npm init 
       npm install socket.io-client
    fi
}