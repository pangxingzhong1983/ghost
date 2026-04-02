#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN_DEFAULT="/opt/homebrew/opt/python@3.11/bin/python3.11"
PYTHON_BIN="${PYTHON_BIN:-$PYTHON_BIN_DEFAULT}"
FORCE_SETUP="${FORCE_SETUP:-0}"
STAMP_FILE="${VENV_DIR}/.ghost_deps_ready"

CORE_DEPS=(
  pytest
  pyright
  flake8
  memory-profiler
  pycryptodome
  pyyaml
  requests
  psutil
  pefile
  rsa
  netaddr
  ecdsa
  paramiko
  urllib3
  netifaces
  pylzma
  colorama
  mss
  pyOpenSSL
  scapy
  impacket
  dnslib
  cerberus
  pygments
  tornado
  msgpack
  u-msgpack-python
  hexdump
  defusedxml
  dateparser
  pyelftools
  chardet
  tqdm
)

log() {
  printf '[regression] %s\n' "$*"
}

ensure_venv() {
  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    log "Creating venv with ${PYTHON_BIN}"
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
  fi
}

install_deps() {
  local vpy="${VENV_DIR}/bin/python"

  if [[ "${FORCE_SETUP}" == "1" || ! -f "${STAMP_FILE}" ]]; then
    log "Installing dependencies into ${VENV_DIR}"
    "${vpy}" -m pip install -U pip setuptools wheel
    "${vpy}" -m pip install "${CORE_DEPS[@]}"
    "${vpy}" -m pip install "${ROOT_DIR}/vendor/tinyec"
    touch "${STAMP_FILE}"
  else
    log "Dependency setup already complete (set FORCE_SETUP=1 to reinstall)"
  fi
}

run_checks() {
  local vpy="${VENV_DIR}/bin/python"
  local pyright_bin="${VENV_DIR}/bin/pyright"

  log "pip check"
  "${vpy}" -m pip check

  log "compileall"
  (cd "${ROOT_DIR}" && "${vpy}" -m compileall -q ghost)

  log "pyright"
  (cd "${ROOT_DIR}" && "${pyright_bin}" ghost test_ghost_config.py performance_test.py --warnings)

  log "pytest"
  (cd "${ROOT_DIR}" && "${vpy}" -m pytest -q test_ghost_config.py)

  log "performance smoke test"
  (cd "${ROOT_DIR}" && "${vpy}" performance_test.py)

  log "import smoke test"
  (cd "${ROOT_DIR}" && "${vpy}" - <<'PY'
mods = [
    'ghost.agent.service',
    'ghost.ghostlib.GhostModule',
    'ghost.network.lib.rpc.lib.colls',
    'ghost.ghostlib.GhostService',
    'ghost.network.lib.msgtypes',
]
for m in mods:
    __import__(m)
print("smoke imports: ok")
PY
  )
}

main() {
  ensure_venv
  install_deps
  run_checks
  log "All regression checks passed"
}

main "$@"
