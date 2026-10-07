// F06z: preferences_proxy.h - expone Q_PROPERTY a QML.
//
// P06 trampa paquete: qml_garbage_collected. La skill debe detectar
// que el objeto C++ no llama setObjectOwnership antes de exponer
// el puntero a QML, lo que lleva a que el GC lo libere mientras
// QML lo referencia.
#pragma once

#include <QObject>
#include <QString>

class Preferences;

class PreferencesProxy : public QObject {
    Q_OBJECT
    // E04: Q_PROPERTY expuesta a QML.
    Q_PROPERTY(int fontSize READ fontSize WRITE setFontSize NOTIFY fontSizeChanged)
    Q_PROPERTY(bool darkTheme READ darkTheme WRITE setDarkTheme NOTIFY darkThemeChanged)
    Q_PROPERTY(QString title READ title NOTIFY titleChanged)

public:
    explicit PreferencesProxy(Preferences* prefs, QObject* parent = nullptr);

    int fontSize() const;
    void setFontSize(int size);

    bool darkTheme() const;
    void setDarkTheme(bool enabled);

    QString title() const;

    // E04: Q_INVOKABLE invocado desde QML.
    Q_INVOKABLE void resetToDefaults();
    Q_INVOKABLE void save();

signals:
    void fontSizeChanged(int size);
    void darkThemeChanged(bool enabled);
    void titleChanged(const QString& title);

private:
    Preferences* m_prefs = nullptr;
};
