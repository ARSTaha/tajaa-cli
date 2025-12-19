#!/bin/bash
# Tajaa Arsenal Installer
# Installs CyberChef, payloads, and wordlists for Tajaa CLI
# Author: Tajaa

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Config
TOOLS_DIR="/opt/tajaa-tools"
CYBERCHEF_VERSION="10.5.2"
CYBERCHEF_URL="https://github.com/gchq/CyberChef/releases/download/v${CYBERCHEF_VERSION}/CyberChef_v${CYBERCHEF_VERSION}.zip"

# Helper functions
print_banner() {
    echo -e "${CYAN}"
    echo "═══════════════════════════════════════════════════════"
    echo "  Tajaa Arsenal Installer"
    echo "  Installing CyberChef, Payloads, and Wordlists"
    echo "═══════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_info() {
    echo -e "${CYAN}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root or with sudo"
        exit 1
    fi
}

check_dependencies() {
    local missing_deps=()

    for cmd in wget unzip firefox; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_info "Install them with: sudo apt install ${missing_deps[*]}"
        exit 1
    fi
}

################################################################################
# Installation Functions
################################################################################

install_cyberchef() {
    print_info "Installing CyberChef (Local HTML version)..."

    local cyberchef_dir="${TOOLS_DIR}/cyberchef"
    local temp_dir="/tmp/cyberchef_install_$$"

    # Create directories
    mkdir -p "$cyberchef_dir"
    mkdir -p "$temp_dir"

    # Download CyberChef
    print_info "Downloading CyberChef v${CYBERCHEF_VERSION}..."
    if wget -q --show-progress -O "${temp_dir}/CyberChef.zip" "$CYBERCHEF_URL"; then
        print_success "Download complete"
    else
        print_error "Failed to download CyberChef"
        rm -rf "$temp_dir"
        return 1
    fi

    # Extract archive
    print_info "Extracting CyberChef..."
    if unzip -q "${temp_dir}/CyberChef.zip" -d "$temp_dir"; then
        print_success "Extraction complete"
    else
        print_error "Failed to extract CyberChef"
        rm -rf "$temp_dir"
        return 1
    fi

    # Find and rename the main HTML file
    local html_file=$(find "$temp_dir" -name "CyberChef_v*.html" -o -name "CyberChef.html" | head -n 1)

    if [[ -z "$html_file" ]]; then
        print_error "CyberChef HTML file not found in archive"
        rm -rf "$temp_dir"
        return 1
    fi

    # Move to final location
    cp "$html_file" "${cyberchef_dir}/CyberChef.html"

    # Set permissions
    chmod 644 "${cyberchef_dir}/CyberChef.html"
    chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$cyberchef_dir"

    # Cleanup
    rm -rf "$temp_dir"

    print_success "CyberChef installed to: ${cyberchef_dir}/CyberChef.html"
    print_info "You can now use the 'cyberchef_local' tool in the CTF Kit"
}

install_wordlists() {
    print_info "Installing common wordlists..."

    # Install SecLists if not present
    if [[ ! -d /usr/share/seclists ]]; then
        print_info "Installing SecLists..."
        apt-get update -qq
        apt-get install -y -qq seclists
        print_success "SecLists installed"
    else
        print_success "SecLists already installed"
    fi

    # Ensure rockyou.txt is extracted
    if [[ -f /usr/share/wordlists/rockyou.txt.gz ]] && [[ ! -f /usr/share/wordlists/rockyou.txt ]]; then
        print_info "Extracting rockyou.txt..."
        gunzip /usr/share/wordlists/rockyou.txt.gz
        print_success "rockyou.txt extracted"
    else
        print_success "rockyou.txt ready"
    fi
}

install_payloads() {
    print_info "Setting up payload directory..."

    local payload_dir="${TOOLS_DIR}/payloads"
    mkdir -p "$payload_dir"

    # Create subdirectories for different payload types
    mkdir -p "${payload_dir}/linux"
    mkdir -p "${payload_dir}/windows"
    mkdir -p "${payload_dir}/web"

    # Download common privilege escalation scripts
    print_info "Downloading LinPEAS..."
    wget -q --show-progress -O "${payload_dir}/linux/linpeas.sh" \
        "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh" || print_warning "LinPEAS download failed"

    print_info "Downloading WinPEAS..."
    wget -q --show-progress -O "${payload_dir}/windows/winpeas.exe" \
        "https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx64.exe" || print_warning "WinPEAS download failed"

    print_info "Downloading pspy64..."
    wget -q --show-progress -O "${payload_dir}/linux/pspy64" \
        "https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64" || print_warning "pspy64 download failed"

    # Set executable permissions
    chmod +x "${payload_dir}/linux/"*.sh 2>/dev/null || true
    chmod +x "${payload_dir}/linux/pspy64" 2>/dev/null || true

    # Set ownership
    chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$payload_dir"

    print_success "Payloads installed to: ${payload_dir}"
    print_info "Start a web server with: cd ${payload_dir} && python3 -m http.server 8000"
}

create_shortcuts() {
    print_info "Creating convenience shortcuts..."

    # Create a shell script to quickly open CyberChef
    cat > /usr/local/bin/cyberchef <<'EOF'
#!/bin/bash
CYBERCHEF_PATH="/opt/tajaa-tools/cyberchef/CyberChef.html"
if [[ -f "$CYBERCHEF_PATH" ]]; then
    firefox "$CYBERCHEF_PATH" &
else
    echo "[!] CyberChef not found. Run: sudo install_arsenal.sh"
    exit 1
fi
EOF

    chmod +x /usr/local/bin/cyberchef
    print_success "Created 'cyberchef' command"
}

show_summary() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                  INSTALLATION COMPLETE                        ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Installed Components:${NC}"
    echo -e "  ${GREEN}✓${NC} CyberChef (Local):  ${TOOLS_DIR}/cyberchef/CyberChef.html"
    echo -e "  ${GREEN}✓${NC} Payloads:           ${TOOLS_DIR}/payloads/"
    echo -e "  ${GREEN}✓${NC} Wordlists:          /usr/share/wordlists/"
    echo ""
    echo -e "${CYAN}Quick Commands:${NC}"
    echo -e "  ${YELLOW}cyberchef${NC}              - Open CyberChef in Firefox"
    echo -e "  ${YELLOW}tajaa${NC}                  - Launch Tajaa CLI"
    echo ""
    echo -e "${CYAN}Payload Server:${NC}"
    echo -e "  ${YELLOW}cd ${TOOLS_DIR}/payloads && python3 -m http.server 8000${NC}"
    echo ""
}

################################################################################
# Main Installation Flow
################################################################################

main() {
    print_banner

    # Pre-flight checks
    check_root
    check_dependencies

    # Create main tools directory
    print_info "Creating tools directory: ${TOOLS_DIR}"
    mkdir -p "$TOOLS_DIR"

    # Install components
    install_cyberchef
    install_wordlists
    install_payloads
    create_shortcuts

    # Show summary
    show_summary

    print_success "Arsenal installation complete!"
    print_info "Run 'tajaa' to launch the framework"
}

# Execute main function
main "$@"

