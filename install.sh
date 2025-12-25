#!/bin/bash
# Tajaa CLI Installation Script
# Handles virtual environment setup automatically
# Author: Tajaa

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Tajaa CLI Installer${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}[1/4]${NC} Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python 3.8+ required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION detected"

# Check if venv module exists
echo -e "${YELLOW}[2/4]${NC} Checking python3-venv..."
if ! python3 -m venv --help &>/dev/null; then
    echo -e "${YELLOW}python3-venv not found. Installing...${NC}"
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install -y python3-venv
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3-virtualenv
    elif command -v pacman &>/dev/null; then
        sudo pacman -S python-virtualenv
    else
        echo -e "${RED}Error: Could not install python3-venv. Please install manually.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓${NC} python3-venv available"

# Create virtual environment
echo -e "${YELLOW}[3/4]${NC} Creating virtual environment..."
if [ -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Recreating...${NC}"
    rm -rf .venv
fi
python3 -m venv .venv
echo -e "${GREEN}✓${NC} Virtual environment created"

# Install dependencies
echo -e "${YELLOW}[4/4]${NC} Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip setuptools wheel >/dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "To use Tajaa CLI:"
echo ""
echo "  1. Activate virtual environment:"
echo -e "     ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "  2. Run Tajaa CLI:"
echo -e "     ${YELLOW}python3 main.py${NC}"
echo ""
echo "  3. Load specific module:"
echo -e "     ${YELLOW}python3 main.py --config configs/02_ctf_kit.yaml${NC}"
echo ""
echo "  4. When finished:"
echo -e "     ${YELLOW}deactivate${NC}"
echo ""
echo "Optional: Create quick aliases (add to ~/.bashrc or ~/.zshrc):"
echo -e "  ${YELLOW}alias tajaa='cd $(pwd) && source .venv/bin/activate && python3 main.py'${NC}"
echo -e "  ${YELLOW}alias tajaa-ctf='cd $(pwd) && source .venv/bin/activate && python3 main.py --config configs/02_ctf_kit.yaml'${NC}"
echo ""

