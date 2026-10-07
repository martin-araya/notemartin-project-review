# fx-swift-ios — Ground truth narrativo

Fixture de app iOS escrito en Swift 6 con SwiftUI, UIKit heredado, un modulo Objective-C expuesto via bridging header, y una extension de widget que comparte datos con la app principal por App Group. La logica testeable vive en un paquete SwiftPM (`Package.swift` con target `FxSwiftCore`); los targets nativos iOS (app + widget) viven en un proyecto Xcode (`Examples/FxSwift.xcodeproj`).

## Stack y toolchain

- **Swift 6** (swift-tools-version 6.0) con toolchain detectado via `DEVELOPER_DIR` apuntando a Xcode 27.0 cuando esta disponible.
- **Plataformas**: `macOS(.v13)` para tests SPM en host, `iOS(.v16)` para los targets Xcode.
- **Frameworks**: SwiftUI, Combine, SwiftData (host fallback), WidgetKit, UIKit, Foundation, AppKit-no.
- **Tests**: Swift Testing (`import Testing` + `@Test` + `@Suite`).
- **Build del Xcode project**: `xcodebuild -project Examples/FxSwift.xcodeproj -scheme FxSwiftApp -destination 'generic/platform=iOS Simulator' -configuration Debug CODE_SIGNING_ALLOWED=NO build`.

## Estructura

```
dev/fixtures/fx-swift-ios/
├── Package.swift                     # SPM con target FxSwiftCore + FxSwiftCoreTests
├── README.md
├── manifest.yml                      # requires: [macos], container.enabled: false
├── Dockerfile.test                   # FROM scratch + CMD false (no contenedor real)
├── Makefile
├── .gitignore
├── unique_tokens.txt
├── build-history.sh                  # 8 commits reproducibles
├── tools/
│   ├── run_spm_and_xcode_tests.sh     # runner principal
│   └── generate_pbxproj.py            # genera project.pbxproj a mano
├── Sources/
│   ├── FxSwiftCore/                   # libreria SPM host-testable
│   │   ├── FxSwiftCore.swift
│   │   ├── AppGroup/                  # AppGroupPaths + AppGroupStore actor (E6, P4)
│   │   ├── Models/                    # Expense, ExpenseCategory, OnboardingState, SyncStatus
│   │   ├── PropertyWrappers/          # @Debounced (E1) + @UserDefaultsBacked
│   │   ├── Protocols/                 # Describable + Describable+Category (E3) + Syncable
│   │   ├── Persistence/               # ExpensesRepository (actor) + ExpensesStore (P3)
│   │   ├── Sync/                      # CloudKitSyncEngine (P1) + SyncCoordinator
│   │   ├── Widget/                    # WidgetSummary, AppGroupReader, WidgetSummaryProvider
│   │   ├── UI/                        # OnboardingView (E2), ExpenseListView, ExpenseRow,
│   │   │                              # DeepLinkRouter (P5), LegacySettingsView
│   │   ├── ObjCBridge/                # LegacyLogger.h/.m + bridging header (E4)
│   │   └── BuildFlags/                # #if os(iOS) / #if DEBUG (E5)
│   └── FxSwiftCoreTests/              # 36 tests Swift Testing en 9 suites
├── Examples/
│   ├── FxSwift.xcodeproj/
│   │   ├── project.pbxproj            # generado por tools/generate_pbxproj.py
│   │   ├── Configs/                   # (vacio: xcconfig en FxSwiftApp/Configs)
│   ├── FxSwiftApp/                    # target iOS app
│   │   ├── AppMain.swift              # @main struct FxSwiftApp con WindowGroup + onOpenURL
│   │   ├── Info.plist                 # CFBundleURLSchemes = [fxswift]
│   │   ├── FxSwiftApp.entitlements    # com.apple.security.application-groups
│   │   ├── FxSwift-Bridging-Header.h
│   │   ├── LegacyLogger.h
│   │   ├── LegacyLogger.m
│   │   ├── SettingsHostController.swift  # UIViewController real con LegacyLogger
│   │   └── Configs/                   # Common.xcconfig, Debug.xcconfig, Release.xcconfig
│   └── FxSwiftWidget/                 # target widget extension
│       ├── WidgetMain.swift           # @main struct FxSwiftWidget + FxSwiftTimelineProvider
│       ├── Info.plist                 # NSExtensionPointIdentifier=com.apple.widgetkit-extension
│       └── FxSwiftWidget.entitlements # mismo App Group
```

## Features (4 x 7 R-NN)

| FEAT | nombre | entry points | trampas relevantes |
|---|---|---|---|
| FEAT-001 | `onboarding` | OnboardingView (NavigationStack) | E2 navigationDestination |
| FEAT-002 | `lista-de-gastos` | ExpenseListView + ExpensesStore | P3 sink sin store, P4 AppGroup |
| FEAT-003 | `sincronizacion-icloud` | CloudKitSyncEngine + SyncCoordinator | P1 silent skip, E1 actor |
| FEAT-004 | `widget-de-resumen` | WidgetSummaryProvider + FxSwiftWidget | E6 App Group, P4 write silencioso |

## Trampas del ecosistema (6)

| id | titulo | archivo |
|---|---|---|
| E01 | Property wrappers | Sources/FxSwiftCore/PropertyWrappers/Debounced.swift:5 |
| E02 | navigationDestination(for:) routing | Sources/FxSwiftCore/UI/OnboardingView.swift:14 |
| E03 | Default impls across files | Sources/FxSwiftCore/Protocols/Describable+Category.swift:9 |
| E04 | Obj-C @objc dynamic + KVO + NSNotificationCenter | Sources/FxSwiftCore/ObjCBridge/LegacyLogger.m:18 |
| E05 | Build flags #if os(iOS) / #if DEBUG | Sources/FxSwiftCore/BuildFlags/BuildFlags.swift:13 |
| E06 | App Group + deep links + URL scheme | Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift:6 |

## Trampas del paquete (6)

| id | titulo | archivo |
|---|---|---|
| P01 | Sync swallows validation errors | Sources/FxSwiftCore/Sync/CloudKitSyncEngine.swift:30 |
| P02 | Widget timeline ignores errors | Sources/FxSwiftCore/Widget/WidgetSummaryProvider.swift:31 |
| P03 | Combine sink without store(in:) | Sources/FxSwiftCore/Persistence/ExpensesStore.swift:31 |
| P04 | AppGroup save swallows errors | Sources/FxSwiftCore/AppGroup/AppGroupStore.swift:31 |
| P05 | Deep link UUID parse swallowed | Sources/FxSwiftCore/UI/DeepLinkRouter.swift:35 |
| P06 | ObjC registerForNotifications not called | Examples/FxSwiftApp/SettingsHostController.swift:36 |

## Trampas superficiales (3)

| id | titulo | archivo |
|---|---|---|
| S01 | Setter in protocol default that ignores value | Sources/FxSwiftCore/Protocols/Syncable.swift:16 |
| S02 | override env var solo usado por tests | Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift:13 |
| S03 | Public init() never called externally | Sources/FxSwiftCore/Sync/CloudKitSyncEngine.swift:21 |

## Limites y decisiones operativas

- `manifest.requires: [macos]` y `container.enabled: false`: el fixture solo corre en macOS con Xcode; los contenedores Linux no pueden validar la parte Xcode ni la Swift Testing API (que viene con Xcode 16+).
- `DEVELOPER_DIR` se detecta automaticamente: si Xcode 27.0 esta en `/System/Volumes/Data/Applications/Xcode.app` o `/Applications/Xcode.app`, el runner lo usa. Si solo hay CommandLineTools, swift build corre pero swift test no encuentra el modulo `Testing` y falla.
- El `Dockerfile.test` existe para que el harness encuentre el archivo; `CMD ["false"]` falla a proposito si alguien intenta construirlo en Linux.
- `project.pbxproj` se genera desde `tools/generate_pbxproj.py` (formato OpenStep plist escrito a mano, IDs derivados de sha1 del nombre). No usamos XcodeGen/Tuist para mantener cero dependencias externas.
- El target `FxSwiftApp` consume `FxSwiftCore` via `XCLocalSwiftPackageReference` (paquete local en `..`); el `package.swift` vive en el directorio padre del `.xcodeproj`.
- El widget extension (`FxSwiftWidget.appex`) se embebe en la app via `PBXCopyFilesBuildPhase` con `dstSubfolderSpec = 13` (PlugIns).
- SettingsHostController.swift vive en `Examples/FxSwiftApp/` (no en `Sources/FxSwiftCore/`) porque solo se compila con el bridging header Obj-C aplicado. `LegacySettingsView` (en FxSwiftCore) usa un placeholder `LegacySettingsHost` que la extension en el target iOS real reemplaza.
