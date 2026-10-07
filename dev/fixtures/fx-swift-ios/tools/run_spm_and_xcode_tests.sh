#!/usr/bin/env bash
# Runner de tests del fixture F06aa.
# 1) Compila y corre los tests Swift Testing del paquete SwiftPM
#    (host macOS). Requiere un toolchain Swift 6 + Testing.framework;
#    se busca primero en Xcode y luego en CommandLineTools.
# 2) Si xcodebuild esta disponible, hace un smoke build del target iOS
#    (Examples/FxSwift.xcodeproj). Si no esta disponible, omite el paso
#    y registra la razon en .build/xcode-skip.log (no falla el fixture).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p .build
LOGDIR="$ROOT/.build"

# Resolver el toolchain a usar. Preferimos Xcode.app (proporciona
# Testing.framework + xcodebuild) si esta disponible; si no,
# usamos el que apunte xcode-select.
if [ -z "${DEVELOPER_DIR:-}" ]; then
    if [ -d "/System/Volumes/Data/Applications/Xcode.app/Contents/Developer" ]; then
        export DEVELOPER_DIR="/System/Volumes/Data/Applications/Xcode.app/Contents/Developer"
    elif [ -d "/Applications/Xcode.app/Contents/Developer" ]; then
        export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
    fi
fi
echo "DEVELOPER_DIR=$DEVELOPER_DIR"

echo "[1/2] swift build + swift test (host macOS)"
swift build 2>&1 | tee "$LOGDIR/spm-build.log"
swift test 2>&1 | tee "$LOGDIR/spm-test.log"

echo "[2/2] xcodebuild build smoke (Examples/FxSwift.xcodeproj)"
if ! command -v xcodebuild >/dev/null 2>&1; then
    echo "xcodebuild no disponible en este host; se omite el smoke build." \
        | tee "$LOGDIR/xcode-skip.log"
    echo "Para validar el target iOS instala Xcode Command Line Tools o Xcode completo."
    exit 0
fi

if ! xcodebuild -version >/dev/null 2>&1; then
    echo "xcodebuild presente pero no funcional (Xcode no instalado). Smoke omitido." \
        | tee "$LOGDIR/xcode-skip.log"
    exit 0
fi

set +e
xcodebuild -project Examples/FxSwift.xcodeproj \
    -scheme FxSwiftApp \
    -destination 'generic/platform=iOS Simulator' \
    -configuration Debug \
    CODE_SIGNING_ALLOWED=NO \
    build 2>&1 | tee "$LOGDIR/xcode-build.log"
rc=${PIPESTATUS[0]}
set -e

if [ "$rc" -ne 0 ]; then
    echo "xcodebuild fallo (rc=$rc). Ver $LOGDIR/xcode-build.log" >&2
    exit "$rc"
fi

echo "OK: swift test + xcodebuild smoke pasaron."
