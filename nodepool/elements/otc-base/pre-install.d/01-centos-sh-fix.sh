#!/bin/bash

if [ "${DIB_DEBUG_TRACE:-0}" -gt 0 ]; then
    set -x
fi
set -eu
set -o pipefail
if [[ ${DISTRO_NAME} =~ (centos) ]]; then
    echo "Applying CentOS-specific /bin/sh fix"
    mkdir -p "$TARGET_ROOT/bin"
    ln -sf /usr/bin/bash "$TARGET_ROOT/bin/sh"
fi
