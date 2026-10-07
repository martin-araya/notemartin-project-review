// F06z: preferences.cpp - implementacion de Preferences con QSettings.
//
// E04: Q_PROPERTY y QSettings. La persistencia usa QSettings con
// la compania y nombre de la aplicacion definidos en main.cpp.
#include "qtapp/preferences.h"

Preferences::Preferences(QObject* parent) : QObject(parent) {
    m_settings = new QSettings(this);
    load();
}

Preferences::~Preferences() {
    if (m_settings) {
        m_settings->sync();
    }
}

void Preferences::setFontSize(int size) {
    if (m_fontSize == size) return;
    m_fontSize = size;
    emit fontSizeChanged(size);
    emit preferencesChanged();
}

void Preferences::setDarkTheme(bool enabled) {
    if (m_darkTheme == enabled) return;
    m_darkTheme = enabled;
    emit darkThemeChanged(enabled);
    emit preferencesChanged();
}

void Preferences::setLegacyProperty(const QString& value) {
    // P03 trampa paquete: q_property_no_notify. Esta propiedad
    // existe pero NO tiene senal NOTIFY. Los bindings de QML no
    // reaccionan al cambio.
    m_legacyProperty = value;
    // NO emitimos ninguna senal: la trampa es esta ausencia.
}

void Preferences::resetToDefaults() {
    setFontSize(12);
    setDarkTheme(false);
    setLegacyProperty("");
}

void Preferences::save() {
    if (!m_settings) return;
    m_settings->setValue("fontSize", m_fontSize);
    m_settings->setValue("darkTheme", m_darkTheme);
    m_settings->setValue("legacyProperty", m_legacyProperty);
    m_settings->sync();
    emit preferencesChanged();
}

void Preferences::load() {
    if (!m_settings) return;
    m_fontSize = m_settings->value("fontSize", 12).toInt();
    m_darkTheme = m_settings->value("darkTheme", false).toBool();
    m_legacyProperty = m_settings->value("legacyProperty", "").toString();
    emit preferencesChanged();
}
