#!/usr/bin/env python3
"""Generador de project.pbxproj minimo para fx-swift-ios.

Crea un proyecto Xcode con dos targets:
- FxSwiftApp: iOS app (depende del package local + extension widget)
- FxSwiftWidget: widget extension embebida en la app

Esta escrito a mano en vez de generarse con XcodeGen o Tuist para
mantener cero dependencias externas. El formato es OpenStep plist.
"""
from __future__ import annotations

import hashlib
import textwrap
from pathlib import Path

PROJECT_NAME = "FxSwift"
BUNDLE_ID_APP = "com.example.fxswift"
BUNDLE_ID_WIDGET = "com.example.fxswift.widget"
DEPLOYMENT_TARGET_IOS = "16.0"

# IDs estables derivados del nombre para que dos regeneraciones
# produzcan el mismo pbxproj.
def _id(name: str) -> str:
    h = hashlib.sha1(name.encode("utf-8")).hexdigest()[:24].upper()
    return h


PROJECT_ID = _id("PBXProject-root")
MAIN_GROUP_ID = _id("PBXGroup-main")
PRODUCTS_GROUP_ID = _id("PBXGroup-products")
APPGROUP_ID = _id("PBXGroup-FxSwiftApp")
WIDGETGROUP_ID = _id("PBXGroup-FxSwiftWidget")
CONFIGSGROUP_ID = _id("PBXGroup-FxSwiftApp-Configs")
APP_TARGET_ID = _id("PBXNativeTarget-FxSwiftApp")
WIDGET_TARGET_ID = _id("PBXNativeTarget-FxSwiftWidget")
WIDGET_PACKAGE_PRODUCT_DEP_ID = _id("XCSwiftPackageProductDependency-FxSwiftCore-Widget")
WIDGET_PACKAGE_PRODUCT_BUILD = _id("PBXBuildFile-FxSwiftCore-Widget")
APP_PRODUCT_ID = _id("PBXFileReference-FxSwiftApp.app")
WIDGET_PRODUCT_ID = _id("PBXFileReference-FxSwiftWidget.appex")
APP_PLIST_ID = _id("PBXFileReference-FxSwiftApp-Info.plist")
WIDGET_PLIST_ID = _id("PBXFileReference-FxSwiftWidget-Info.plist")
APP_ENT_ID = _id("PBXFileReference-FxSwiftApp.entitlements")
WIDGET_ENT_ID = _id("PBXFileReference-FxSwiftWidget.entitlements")
APPMAIN_ID = _id("PBXFileReference-AppMain.swift")
WIDGETMAIN_ID = _id("PBXFileReference-WidgetMain.swift")
SETTINGS_HOST_CTRL_ID = _id("PBXFileReference-SettingsHostController.swift")
SETTINGS_HOST_CTRL_BUILD = _id("PBXBuildFile-SettingsHostController.swift")
DEBUG_CONFIG_ID = _id("XCBuildConfiguration-Debug")
RELEASE_CONFIG_ID = _id("XCBuildConfiguration-Release")
DEBUG_XCCONFIG_ID = _id("PBXFileReference-Debug.xcconfig")
RELEASE_XCCONFIG_ID = _id("PBXFileReference-Release.xcconfig")
TARGET_CONFIG_LIST_APP = _id("XCConfigurationList-FxSwiftApp")
TARGET_CONFIG_LIST_WIDGET = _id("XCConfigurationList-FxSwiftWidget")
PROJECT_CONFIG_LIST = _id("XCConfigurationList-root")
APP_DEBUG_CONFIG_ID = _id("XCBuildConfiguration-FxSwiftApp-Debug")
APP_RELEASE_CONFIG_ID = _id("XCBuildConfiguration-FxSwiftApp-Release")
WIDGET_DEBUG_CONFIG_ID = _id("XCBuildConfiguration-FxSwiftWidget-Debug")
WIDGET_RELEASE_CONFIG_ID = _id("XCBuildConfiguration-FxSwiftWidget-Release")
APP_SOURCES_PHASE = _id("PBXSourcesBuildPhase-FxSwiftApp")
WIDGET_SOURCES_PHASE = _id("PBXSourcesBuildPhase-FxSwiftWidget")
APP_FRAMEWORKS_PHASE = _id("PBXFrameworksBuildPhase-FxSwiftApp")
WIDGET_FRAMEWORKS_PHASE = _id("PBXFrameworksBuildPhase-FxSwiftWidget")
APP_RESOURCES_PHASE = _id("PBXResourcesBuildPhase-FxSwiftApp")
WIDGET_RESOURCES_PHASE = _id("PBXResourcesBuildPhase-FxSwiftWidget")
APP_EMBED_PHASE = _id("PBXCopyFilesBuildPhase-Embed-FxSwiftApp")
APP_DEPENDENCY_ID = _id("PBXTargetDependency-FxSwiftApp-FxSwiftWidget")
CONTAINER_ITEM_PROXY_ID = _id("PBXContainerItemProxy-FxSwiftApp-FxSwiftWidget")
SWIFT_PACKAGE_REF = _id("XCRemoteSwiftPackageReference-FxSwiftCore")
PRODUCT_DEPENDENCY_ID = _id("XCSwiftPackageProductDependency-FxSwiftCore")
BRIDGING_HEADER_REF = _id("PBXFileReference-FxSwift-Bridging-Header")
LEGACY_LOGGER_H_REF = _id("PBXFileReference-LegacyLogger.h")
LEGACY_LOGGER_M_REF = _id("PBXFileReference-LegacyLogger.m")
LEGACY_LOGGER_M_BUILD = _id("PBXBuildFile-LegacyLogger.m")
APPMAIN_BUILD = _id("PBXBuildFile-AppMain.swift")
WIDGETMAIN_BUILD = _id("PBXBuildFile-WidgetMain.swift")
APP_PLIST_BUILD = _id("PBXBuildFile-FxSwiftApp-Info.plist")
WIDGET_PLIST_BUILD = _id("PBXBuildFile-FxSwiftWidget-Info.plist")
WIDGET_PRODUCT_BUILD = _id("PBXBuildFile-FxSwiftWidget-appex")
PRODUCT_DEP_BUILD = _id("PBXBuildFile-FxSwiftCore")


def render() -> str:
    return textwrap.dedent(f"""\
        // !$*UTF8*$!
        {{
        \tarchiveVersion = 1;
        \tclasses = {{
        \t}};
        \tobjectVersion = 56;
        \tobjects = {{

        /* Begin PBXBuildFile section */
        \t\t{APPMAIN_BUILD} /* AppMain.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {APPMAIN_ID} /* AppMain.swift */; }};
        \t\t{SETTINGS_HOST_CTRL_BUILD} /* SettingsHostController.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {SETTINGS_HOST_CTRL_ID} /* SettingsHostController.swift */; }};
        \t\t{WIDGETMAIN_BUILD} /* WidgetMain.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {WIDGETMAIN_ID} /* WidgetMain.swift */; }};
        \t\t{APP_PLIST_BUILD} /* Info.plist in Resources */ = {{isa = PBXBuildFile; fileRef = {APP_PLIST_ID} /* Info.plist */; }};
        \t\t{WIDGET_PLIST_BUILD} /* Info.plist in Resources */ = {{isa = PBXBuildFile; fileRef = {WIDGET_PLIST_ID} /* Info.plist */; }};
        \t\t{LEGACY_LOGGER_M_BUILD} /* LegacyLogger.m in Sources */ = {{isa = PBXBuildFile; fileRef = {LEGACY_LOGGER_M_REF} /* LegacyLogger.m */; }};
        \t\t{PRODUCT_DEP_BUILD} /* FxSwiftCore in Frameworks */ = {{isa = PBXBuildFile; productRef = {PRODUCT_DEPENDENCY_ID} /* FxSwiftCore */; }};
        \t\t{WIDGET_PACKAGE_PRODUCT_BUILD} /* FxSwiftCore in Frameworks */ = {{isa = PBXBuildFile; productRef = {WIDGET_PACKAGE_PRODUCT_DEP_ID} /* FxSwiftCore */; }};
        \t\t{WIDGET_PRODUCT_BUILD} /* FxSwiftWidget.appex in Embed Foundation Extensions */ = {{isa = PBXBuildFile; fileRef = {WIDGET_PRODUCT_ID} /* FxSwiftWidget.appex */; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};
        /* End PBXBuildFile section */

        /* Begin PBXContainerItemProxy section */
        \t\t{CONTAINER_ITEM_PROXY_ID} /* PBXContainerItemProxy */ = {{
        \t\t\tisa = PBXContainerItemProxy;
        \t\t\tcontainerPortal = {PROJECT_ID} /* Project object */;
        \t\t\tproxyType = 1;
        \t\t\tremoteGlobalIDString = {WIDGET_TARGET_ID};
        \t\t\tremoteInfo = FxSwiftWidget;
        \t\t}};
        /* End PBXContainerItemProxy section */

        /* Begin PBXCopyFilesBuildPhase section */
        \t\t{APP_EMBED_PHASE} /* Embed Foundation Extensions */ = {{
        \t\t\tisa = PBXCopyFilesBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tdstPath = "";
        \t\t\tdstSubfolderSpec = 13;
        \t\t\tfiles = (
        \t\t\t\t{WIDGET_PRODUCT_BUILD} /* FxSwiftWidget.appex in Embed Foundation Extensions */,
        \t\t\t);
        \t\t\tname = "Embed Foundation Extensions";
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        /* End PBXCopyFilesBuildPhase section */

        /* Begin PBXFileReference section */
        \t\t{APP_PRODUCT_ID} /* FxSwiftApp.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = FxSwiftApp.app; sourceTree = BUILT_PRODUCTS_DIR; }};
        \t\t{WIDGET_PRODUCT_ID} /* FxSwiftWidget.appex */ = {{isa = PBXFileReference; explicitFileType = "wrapper.app-extension"; includeInIndex = 0; path = FxSwiftWidget.appex; sourceTree = BUILT_PRODUCTS_DIR; }};
        \t\t{APP_PLIST_ID} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
        \t\t{WIDGET_PLIST_ID} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
        \t\t{APP_ENT_ID} /* FxSwiftApp.entitlements */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.entitlements; path = FxSwiftApp.entitlements; sourceTree = "<group>"; }};
        \t\t{WIDGET_ENT_ID} /* FxSwiftWidget.entitlements */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.entitlements; path = FxSwiftWidget.entitlements; sourceTree = "<group>"; }};
        \t\t{APPMAIN_ID} /* AppMain.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AppMain.swift; sourceTree = "<group>"; }};
        \t\t{SETTINGS_HOST_CTRL_ID} /* SettingsHostController.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = SettingsHostController.swift; sourceTree = "<group>"; }};
        \t\t{WIDGETMAIN_ID} /* WidgetMain.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = WidgetMain.swift; sourceTree = "<group>"; }};
        \t\t{DEBUG_XCCONFIG_ID} /* Debug.xcconfig */ = {{isa = PBXFileReference; lastKnownFileType = text.xcconfig; path = Debug.xcconfig; sourceTree = "<group>"; }};
        \t\t{RELEASE_XCCONFIG_ID} /* Release.xcconfig */ = {{isa = PBXFileReference; lastKnownFileType = text.xcconfig; path = Release.xcconfig; sourceTree = "<group>"; }};
        \t\t{BRIDGING_HEADER_REF} /* FxSwift-Bridging-Header.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = "FxSwift-Bridging-Header.h"; sourceTree = "<group>"; }};
        \t\t{LEGACY_LOGGER_H_REF} /* LegacyLogger.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = LegacyLogger.h; sourceTree = "<group>"; }};
        \t\t{LEGACY_LOGGER_M_REF} /* LegacyLogger.m */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = LegacyLogger.m; sourceTree = "<group>"; }};
        /* End PBXFileReference section */

        /* Begin PBXFrameworksBuildPhase section */
        \t\t{APP_FRAMEWORKS_PHASE} /* Frameworks */ = {{
        \t\t\tisa = PBXFrameworksBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t\t{PRODUCT_DEP_BUILD} /* FxSwiftCore in Frameworks */,
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        \t\t{WIDGET_FRAMEWORKS_PHASE} /* Frameworks */ = {{
        \t\t\tisa = PBXFrameworksBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t\t{WIDGET_PACKAGE_PRODUCT_BUILD} /* FxSwiftCore in Frameworks */,
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        /* End PBXFrameworksBuildPhase section */

        /* Begin PBXGroup section */
        \t\t{MAIN_GROUP_ID} = {{
        \t\t\tisa = PBXGroup;
        \t\t\tchildren = (
        \t\t\t\t{APPGROUP_ID} /* FxSwiftApp */,
        \t\t\t\t{WIDGETGROUP_ID} /* FxSwiftWidget */,
        \t\t\t\t{PRODUCTS_GROUP_ID} /* Products */,
        \t\t\t);
        \t\t\tsourceTree = "<group>";
        \t\t}};
        \t\t{PRODUCTS_GROUP_ID} /* Products */ = {{
        \t\t\tisa = PBXGroup;
        \t\t\tchildren = (
        \t\t\t\t{APP_PRODUCT_ID} /* FxSwiftApp.app */,
        \t\t\t\t{WIDGET_PRODUCT_ID} /* FxSwiftWidget.appex */,
        \t\t\t);
        \t\t\tname = Products;
        \t\t\tsourceTree = "<group>";
        \t\t}};
        \t\t{APPGROUP_ID} /* FxSwiftApp */ = {{
        \t\t\tisa = PBXGroup;
        \t\t\tchildren = (
        \t\t\t\t{APPMAIN_ID} /* AppMain.swift */,
        \t\t\t\t{SETTINGS_HOST_CTRL_ID} /* SettingsHostController.swift */,
        \t\t\t\t{APP_PLIST_ID} /* Info.plist */,
        \t\t\t\t{APP_ENT_ID} /* FxSwiftApp.entitlements */,
        \t\t\t\t{BRIDGING_HEADER_REF} /* FxSwift-Bridging-Header.h */,
        \t\t\t\t{LEGACY_LOGGER_H_REF} /* LegacyLogger.h */,
        \t\t\t\t{LEGACY_LOGGER_M_REF} /* LegacyLogger.m */,
        \t\t\t\t{CONFIGSGROUP_ID} /* Configs */,
        \t\t\t);
        \t\t\tpath = FxSwiftApp;
        \t\t\tsourceTree = "<group>";
        \t\t}};
        \t\t{WIDGETGROUP_ID} /* FxSwiftWidget */ = {{
        \t\t\tisa = PBXGroup;
        \t\t\tchildren = (
        \t\t\t\t{WIDGETMAIN_ID} /* WidgetMain.swift */,
        \t\t\t\t{WIDGET_PLIST_ID} /* Info.plist */,
        \t\t\t\t{WIDGET_ENT_ID} /* FxSwiftWidget.entitlements */,
        \t\t\t);
        \t\t\tpath = FxSwiftWidget;
        \t\t\tsourceTree = "<group>";
        \t\t}};
        \t\t{CONFIGSGROUP_ID} /* Configs */ = {{
        \t\t\tisa = PBXGroup;
        \t\t\tchildren = (
        \t\t\t\t{DEBUG_XCCONFIG_ID} /* Debug.xcconfig */,
        \t\t\t\t{RELEASE_XCCONFIG_ID} /* Release.xcconfig */,
        \t\t\t);
        \t\t\tpath = Configs;
        \t\t\tsourceTree = "<group>";
        \t\t}};
        /* End PBXGroup section */

        /* Begin PBXNativeTarget section */
        \t\t{APP_TARGET_ID} /* FxSwiftApp */ = {{
        \t\t\tisa = PBXNativeTarget;
        \t\t\tbuildConfigurationList = {TARGET_CONFIG_LIST_APP} /* Build configuration list for PBXNativeTarget "FxSwiftApp" */;
        \t\t\tbuildPhases = (
        \t\t\t\t{APP_SOURCES_PHASE} /* Sources */,
        \t\t\t\t{APP_FRAMEWORKS_PHASE} /* Frameworks */,
        \t\t\t\t{APP_RESOURCES_PHASE} /* Resources */,
        \t\t\t\t{APP_EMBED_PHASE} /* Embed Foundation Extensions */,
        \t\t\t);
        \t\t\tbuildRules = (
        \t\t\t);
        \t\t\tdependencies = (
        \t\t\t\t{APP_DEPENDENCY_ID} /* PBXTargetDependency */,
        \t\t\t);
        \t\t\tname = FxSwiftApp;
        \t\t\tpackageProductDependencies = (
        \t\t\t\t{PRODUCT_DEPENDENCY_ID} /* FxSwiftCore */,
        \t\t\t);
        \t\t\tproductName = FxSwiftApp;
        \t\t\tproductReference = {APP_PRODUCT_ID} /* FxSwiftApp.app */;
        \t\t\tproductType = "com.apple.product-type.application";
        \t\t}};
        \t\t{WIDGET_TARGET_ID} /* FxSwiftWidget */ = {{
        \t\t\tisa = PBXNativeTarget;
        \t\t\tbuildConfigurationList = {TARGET_CONFIG_LIST_WIDGET} /* Build configuration list for PBXNativeTarget "FxSwiftWidget" */;
        \t\t\tbuildPhases = (
        \t\t\t\t{WIDGET_SOURCES_PHASE} /* Sources */,
        \t\t\t\t{WIDGET_FRAMEWORKS_PHASE} /* Frameworks */,
        \t\t\t\t{WIDGET_RESOURCES_PHASE} /* Resources */,
        \t\t\t);
        \t\t\tbuildRules = (
        \t\t\t);
        \t\t\tdependencies = (
        \t\t\t);
        \t\t\tname = FxSwiftWidget;
        \t\t\tpackageProductDependencies = (
        \t\t\t\t{WIDGET_PACKAGE_PRODUCT_DEP_ID} /* FxSwiftCore */,
        \t\t\t);
        \t\t\tproductName = FxSwiftWidget;
        \t\t\tproductReference = {WIDGET_PRODUCT_ID} /* FxSwiftWidget.appex */;
        \t\t\tproductType = "com.apple.product-type.app-extension";
        \t\t}};
        /* End PBXNativeTarget section */

        /* Begin PBXProject section */
        \t\t{PROJECT_ID} /* Project object */ = {{
        \t\t\tisa = PBXProject;
        \t\t\tattributes = {{
        \t\t\t\tBuildIndependentTargetsInParallel = YES;
        \t\t\t\tLastSwiftUpdateCheck = 1500;
        \t\t\t\tLastUpgradeCheck = 1500;
        \t\t\t\tTargetAttributes = {{
        \t\t\t\t\t{APP_TARGET_ID} = {{
        \t\t\t\t\t\tCreatedOnToolsVersion = 15.0;
        \t\t\t\t\t}};
        \t\t\t\t\t{WIDGET_TARGET_ID} = {{
        \t\t\t\t\t\tCreatedOnToolsVersion = 15.0;
        \t\t\t\t\t}};
        \t\t\t\t}};
        \t\t\t}};
        \t\t\tbuildConfigurationList = {PROJECT_CONFIG_LIST} /* Build configuration list for PBXProject "{PROJECT_NAME}" */;
        \t\t\tcompatibilityVersion = "Xcode 14.0";
        \t\t\tdevelopmentRegion = en;
        \t\t\thasScannedForEncodings = 0;
        \t\t\tknownRegions = (
        \t\t\t\ten,
        \t\t\t\tBase,
        \t\t\t);
        \t\t\tmainGroup = {MAIN_GROUP_ID};
        \t\t\tpackageReferences = (
        \t\t\t\t{SWIFT_PACKAGE_REF} /* XCRemoteSwiftPackageReference "FxSwiftCore" */,
        \t\t\t);
        \t\t\tproductRefGroup = {PRODUCTS_GROUP_ID} /* Products */;
        \t\t\tprojectDirPath = "";
        \t\t\tprojectRoot = "";
        \t\t\ttargets = (
        \t\t\t\t{APP_TARGET_ID} /* FxSwiftApp */,
        \t\t\t\t{WIDGET_TARGET_ID} /* FxSwiftWidget */,
        \t\t\t);
        \t\t}};
        /* End PBXProject section */

        /* Begin PBXResourcesBuildPhase section */
        \t\t{APP_RESOURCES_PHASE} /* Resources */ = {{
        \t\t\tisa = PBXResourcesBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        \t\t{WIDGET_RESOURCES_PHASE} /* Resources */ = {{
        \t\t\tisa = PBXResourcesBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        /* End PBXResourcesBuildPhase section */

        /* Begin PBXSourcesBuildPhase section */
        \t\t{APP_SOURCES_PHASE} /* Sources */ = {{
        \t\t\tisa = PBXSourcesBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t\t{APPMAIN_BUILD} /* AppMain.swift in Sources */,
        \t\t\t\t{SETTINGS_HOST_CTRL_BUILD} /* SettingsHostController.swift in Sources */,
        \t\t\t\t{LEGACY_LOGGER_M_BUILD} /* LegacyLogger.m in Sources */,
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        \t\t{WIDGET_SOURCES_PHASE} /* Sources */ = {{
        \t\t\tisa = PBXSourcesBuildPhase;
        \t\t\tbuildActionMask = 2147483647;
        \t\t\tfiles = (
        \t\t\t\t{WIDGETMAIN_BUILD} /* WidgetMain.swift in Sources */,
        \t\t\t);
        \t\t\trunOnlyForDeploymentPostprocessing = 0;
        \t\t}};
        /* End PBXSourcesBuildPhase section */

        /* Begin PBXTargetDependency section */
        \t\t{APP_DEPENDENCY_ID} /* PBXTargetDependency */ = {{
        \t\t\tisa = PBXTargetDependency;
        \t\t\ttarget = {WIDGET_TARGET_ID} /* FxSwiftWidget */;
        \t\t\ttargetProxy = {CONTAINER_ITEM_PROXY_ID} /* PBXContainerItemProxy */;
        \t\t}};
        /* End PBXTargetDependency section */

        /* Begin XCBuildConfiguration section */
        \t\t{DEBUG_CONFIG_ID} /* Debug */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbuildSettings = {{
        \t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;
        \t\t\t\tCLANG_ANALYZER_NONNULL = YES;
        \t\t\t\tCLANG_ENABLE_MODULES = YES;
        \t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;
        \t\t\t\tCOPY_PHASE_STRIP = NO;
        \t\t\t\tDEBUG_INFORMATION_FORMAT = dwarf;
        \t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;
        \t\t\t\tENABLE_TESTABILITY = YES;
        \t\t\t\tGCC_C_LANGUAGE_STANDARD = gnu17;
        \t\t\t\tGCC_DYNAMIC_NO_PIC = NO;
        \t\t\t\tGCC_NO_COMMON_BLOCKS = YES;
        \t\t\t\tGCC_OPTIMIZATION_LEVEL = 0;
        \t\t\t\tGCC_PREPROCESSOR_DEFINITIONS = (
        \t\t\t\t\t"DEBUG=1",
        \t\t\t\t\t"$(inherited)",
        \t\t\t\t);
        \t\t\t\tIPHONEOS_DEPLOYMENT_TARGET = {DEPLOYMENT_TARGET_IOS};
        \t\t\t\tMTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
        \t\t\t\tMTL_FAST_MATH = YES;
        \t\t\t\tONLY_ACTIVE_ARCH = YES;
        \t\t\t\tSDKROOT = iphoneos;
        \t\t\t\tSWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
        \t\t\t\tSWIFT_OPTIMIZATION_LEVEL = "-Onone";
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t}};
        \t\t\tname = Debug;
        \t\t}};
        \t\t{RELEASE_CONFIG_ID} /* Release */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbuildSettings = {{
        \t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;
        \t\t\t\tCLANG_ANALYZER_NONNULL = YES;
        \t\t\t\tCLANG_ENABLE_MODULES = YES;
        \t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;
        \t\t\t\tCOPY_PHASE_STRIP = NO;
        \t\t\t\tDEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
        \t\t\t\tENABLE_NS_ASSERTIONS = NO;
        \t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;
        \t\t\t\tGCC_C_LANGUAGE_STANDARD = gnu17;
        \t\t\t\tGCC_NO_COMMON_BLOCKS = YES;
        \t\t\t\tIPHONEOS_DEPLOYMENT_TARGET = {DEPLOYMENT_TARGET_IOS};
        \t\t\t\tMTL_ENABLE_DEBUG_INFO = NO;
        \t\t\t\tMTL_FAST_MATH = YES;
        \t\t\t\tSDKROOT = iphoneos;
        \t\t\t\tSWIFT_COMPILATION_MODE = wholemodule;
        \t\t\t\tSWIFT_OPTIMIZATION_LEVEL = "-O";
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t\tVALIDATE_PRODUCT = YES;
        \t\t\t}};
        \t\t\tname = Release;
        \t\t}};
        \t\t{APP_DEBUG_CONFIG_ID} /* Debug */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbaseConfigurationReference = {DEBUG_XCCONFIG_ID} /* Debug.xcconfig */;
        \t\t\tbuildSettings = {{
        \t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
        \t\t\t\tCODE_SIGN_ENTITLEMENTS = FxSwiftApp/FxSwiftApp.entitlements;
        \t\t\t\tCODE_SIGN_STYLE = Automatic;
        \t\t\t\tCURRENT_PROJECT_VERSION = 1;
        \t\t\t\tENABLE_PREVIEWS = YES;
        \t\t\t\tGENERATE_INFOPLIST_FILE = NO;
        \t\t\t\tINFOPLIST_FILE = FxSwiftApp/Info.plist;
        \t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
        \t\t\t\t\t"$(inherited)",
        \t\t\t\t\t"@executable_path/Frameworks",
        \t\t\t\t);
        \t\t\t\tMARKETING_VERSION = 1.0;
        \t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = "{BUNDLE_ID_APP}";
        \t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
        \t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
        \t\t\t\tSWIFT_OBJC_BRIDGING_HEADER = "FxSwiftApp/FxSwift-Bridging-Header.h";
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
        \t\t\t}};
        \t\t\tname = Debug;
        \t\t}};
        \t\t{APP_RELEASE_CONFIG_ID} /* Release */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbaseConfigurationReference = {RELEASE_XCCONFIG_ID} /* Release.xcconfig */;
        \t\t\tbuildSettings = {{
        \t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
        \t\t\t\tCODE_SIGN_ENTITLEMENTS = FxSwiftApp/FxSwiftApp.entitlements;
        \t\t\t\tCODE_SIGN_STYLE = Automatic;
        \t\t\t\tCURRENT_PROJECT_VERSION = 1;
        \t\t\t\tENABLE_PREVIEWS = YES;
        \t\t\t\tGENERATE_INFOPLIST_FILE = NO;
        \t\t\t\tINFOPLIST_FILE = FxSwiftApp/Info.plist;
        \t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
        \t\t\t\t\t"$(inherited)",
        \t\t\t\t\t"@executable_path/Frameworks",
        \t\t\t\t);
        \t\t\t\tMARKETING_VERSION = 1.0;
        \t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = "{BUNDLE_ID_APP}";
        \t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
        \t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
        \t\t\t\tSWIFT_OBJC_BRIDGING_HEADER = "FxSwiftApp/FxSwift-Bridging-Header.h";
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
        \t\t\t}};
        \t\t\tname = Release;
        \t\t}};
        \t\t{WIDGET_DEBUG_CONFIG_ID} /* Debug */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbaseConfigurationReference = {DEBUG_XCCONFIG_ID} /* Debug.xcconfig */;
        \t\t\tbuildSettings = {{
        \t\t\t\tCODE_SIGN_ENTITLEMENTS = FxSwiftWidget/FxSwiftWidget.entitlements;
        \t\t\t\tCODE_SIGN_STYLE = Automatic;
        \t\t\t\tCURRENT_PROJECT_VERSION = 1;
        \t\t\t\tGENERATE_INFOPLIST_FILE = NO;
        \t\t\t\tINFOPLIST_FILE = FxSwiftWidget/Info.plist;
        \t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
        \t\t\t\t\t"$(inherited)",
        \t\t\t\t\t"@executable_path/Frameworks",
        \t\t\t\t\t"@executable_path/../../Frameworks",
        \t\t\t\t);
        \t\t\t\tMARKETING_VERSION = 1.0;
        \t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = "{BUNDLE_ID_WIDGET}";
        \t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
        \t\t\t\tSKIP_INSTALL = YES;
        \t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
        \t\t\t}};
        \t\t\tname = Debug;
        \t\t}};
        \t\t{WIDGET_RELEASE_CONFIG_ID} /* Release */ = {{
        \t\t\tisa = XCBuildConfiguration;
        \t\t\tbaseConfigurationReference = {RELEASE_XCCONFIG_ID} /* Release.xcconfig */;
        \t\t\tbuildSettings = {{
        \t\t\t\tCODE_SIGN_ENTITLEMENTS = FxSwiftWidget/FxSwiftWidget.entitlements;
        \t\t\t\tCODE_SIGN_STYLE = Automatic;
        \t\t\t\tCURRENT_PROJECT_VERSION = 1;
        \t\t\t\tGENERATE_INFOPLIST_FILE = NO;
        \t\t\t\tINFOPLIST_FILE = FxSwiftWidget/Info.plist;
        \t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
        \t\t\t\t\t"$(inherited)",
        \t\t\t\t\t"@executable_path/Frameworks",
        \t\t\t\t\t"@executable_path/../../Frameworks",
        \t\t\t\t);
        \t\t\t\tMARKETING_VERSION = 1.0;
        \t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = "{BUNDLE_ID_WIDGET}";
        \t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
        \t\t\t\tSKIP_INSTALL = YES;
        \t\t\t\tSWIFT_EMIT_LOC_STRINGS = YES;
        \t\t\t\tSWIFT_VERSION = 5.0;
        \t\t\t\tTARGETED_DEVICE_FAMILY = "1,2";
        \t\t\t}};
        \t\t\tname = Release;
        \t\t}};
        /* End XCBuildConfiguration section */

        /* Begin XCConfigurationList section */
        \t\t{PROJECT_CONFIG_LIST} /* Build configuration list for PBXProject "{PROJECT_NAME}" */ = {{
        \t\t\tisa = XCConfigurationList;
        \t\t\tbuildConfigurations = (
        \t\t\t\t{DEBUG_CONFIG_ID} /* Debug */,
        \t\t\t\t{RELEASE_CONFIG_ID} /* Release */,
        \t\t\t);
        \t\t\tdefaultConfigurationIsVisible = 0;
        \t\t\tdefaultConfigurationName = Release;
        \t\t}};
        \t\t{TARGET_CONFIG_LIST_APP} /* Build configuration list for PBXNativeTarget "FxSwiftApp" */ = {{
        \t\t\tisa = XCConfigurationList;
        \t\t\tbuildConfigurations = (
        \t\t\t\t{APP_DEBUG_CONFIG_ID} /* Debug */,
        \t\t\t\t{APP_RELEASE_CONFIG_ID} /* Release */,
        \t\t\t);
        \t\t\tdefaultConfigurationIsVisible = 0;
        \t\t\tdefaultConfigurationName = Release;
        \t\t}};
        \t\t{TARGET_CONFIG_LIST_WIDGET} /* Build configuration list for PBXNativeTarget "FxSwiftWidget" */ = {{
        \t\t\tisa = XCConfigurationList;
        \t\t\tbuildConfigurations = (
        \t\t\t\t{WIDGET_DEBUG_CONFIG_ID} /* Debug */,
        \t\t\t\t{WIDGET_RELEASE_CONFIG_ID} /* Release */,
        \t\t\t);
        \t\t\tdefaultConfigurationIsVisible = 0;
        \t\t\tdefaultConfigurationName = Release;
        \t\t}};
        /* End XCConfigurationList section */

        /* Begin XCLocalSwiftPackageReference section */
        \t\t{SWIFT_PACKAGE_REF} /* XCLocalSwiftPackageReference "FxSwiftCore" */ = {{
        \t\t\tisa = XCLocalSwiftPackageReference;
        \t\t\trelativePath = ..;
        \t\t}};
        /* End XCLocalSwiftPackageReference section */

        /* Begin XCSwiftPackageProductDependency section */
        \t\t{PRODUCT_DEPENDENCY_ID} /* FxSwiftCore */ = {{
        \t\t\tisa = XCSwiftPackageProductDependency;
        \t\t\tpackage = {SWIFT_PACKAGE_REF} /* XCLocalSwiftPackageReference "FxSwiftCore" */;
        \t\t\tproductName = FxSwiftCore;
        \t\t}};
        \t\t{WIDGET_PACKAGE_PRODUCT_DEP_ID} /* FxSwiftCore */ = {{
        \t\t\tisa = XCSwiftPackageProductDependency;
        \t\t\tpackage = {SWIFT_PACKAGE_REF} /* XCLocalSwiftPackageReference "FxSwiftCore" */;
        \t\t\tproductName = FxSwiftCore;
        \t\t}};
        /* End XCSwiftPackageProductDependency section */
        \t}};
        \trootObject = {PROJECT_ID} /* Project object */;
        }}
        """)


def main() -> int:
    out = Path(__file__).resolve().parent.parent / "Examples" / "FxSwift.xcodeproj" / "project.pbxproj"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
