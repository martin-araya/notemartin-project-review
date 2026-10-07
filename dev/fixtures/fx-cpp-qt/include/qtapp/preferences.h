// F06z: preferences.h - QObject con Q_PROPERTY y QSettings.
//
// E04: Q_PROPERTY expone propiedades a QML via meta-object. Q_INVOKABLE
// expone metodos invocables desde QML. La trampa paquete P03
// (q_property_no_notify) planta una propiedad sin NOTIFY.
#pragma once

#include <QObject>
#include <QSettings>

class Preferences : public QObject {
    Q_OBJECT
    // E04: Q_PROPERTY con NOTIFY. Los bindings de QML se actualizan
    // cuando emitimos esta senal.
    Q_PROPERTY(int fontSize READ fontSize WRITE setFontSize NOTIFY fontSizeChanged)
    Q_PROPERTY(bool darkTheme READ darkTheme WRITE setDarkTheme NOTIFY darkThemeChanged)

    // P03 trampa paquete: Q_PROPERTY sin NOTIFY. Los bindings de QML
    // no se actualizan cuando cambia. Documentado y verificado.
    Q_PROPERTY(QString legacyProperty READ legacyProperty WRITE setLegacyProperty)

public:
    explicit Preferences(QObject* parent = nullptr);
    ~Preferences() override;

    int fontSize() const { return m_fontSize; }
    void setFontSize(int size);

    bool darkTheme() const { return m_darkTheme; }
    void setDarkTheme(bool enabled);

    QString legacyProperty() const { return m_legacyProperty; }
    void setLegacyProperty(const QString& value);

    // E04: Q_INVOKABLE expuesto a QML.
    Q_INVOKABLE void resetToDefaults();
    Q_INVOKABLE void save();
    Q_INVOKABLE void load();

signals:
    void fontSizeChanged(int size);
    void darkThemeChanged(bool enabled);
    // S01: senal emitida sin connect.
    void preferencesChanged();

private:
    QSettings* m_settings = nullptr;
    int m_fontSize = 12;
    bool m_darkTheme = false;
    QString m_legacyProperty;
};
