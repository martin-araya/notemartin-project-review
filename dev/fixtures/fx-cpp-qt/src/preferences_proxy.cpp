// F06z: preferences_proxy.cpp - proxy para exponer Preferences a QML.
//
// P06 trampa paquete: qml_garbage_collected. La skill debe detectar
// que el proxy se expone a QML sin setObjectOwnership, lo que
// permite que el GC de QML lo libere mientras QML lo referencia.
#include "qtapp/preferences_proxy.h"
#include "qtapp/preferences.h"

PreferencesProxy::PreferencesProxy(Preferences* prefs, QObject* parent)
    : QObject(parent), m_prefs(prefs) {
    if (m_prefs) {
        // P06 trampa: NO llamamos setObjectOwnership. La instancia
        // queda con CppOwnership por defecto, lo que significa que
        // QML puede recolectar este objeto como basura si no hay
        // referencia JavaScript viva.
        connect(m_prefs, &Preferences::fontSizeChanged, this, &PreferencesProxy::fontSizeChanged);
        connect(m_prefs, &Preferences::darkThemeChanged, this, &PreferencesProxy::darkThemeChanged);
    }
}

int PreferencesProxy::fontSize() const {
    return m_prefs ? m_prefs->fontSize() : 12;
}

void PreferencesProxy::setFontSize(int size) {
    if (m_prefs) m_prefs->setFontSize(size);
}

bool PreferencesProxy::darkTheme() const {
    return m_prefs ? m_prefs->darkTheme() : false;
}

void PreferencesProxy::setDarkTheme(bool enabled) {
    if (m_prefs) m_prefs->setDarkTheme(enabled);
}

QString PreferencesProxy::title() const {
    return QString("fxproc Qt App - Font %1").arg(fontSize());
}

void PreferencesProxy::resetToDefaults() {
    if (m_prefs) m_prefs->resetToDefaults();
}

void PreferencesProxy::save() {
    if (m_prefs) m_prefs->save();
}
