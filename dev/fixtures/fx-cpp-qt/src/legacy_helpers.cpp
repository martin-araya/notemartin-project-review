// F06z: legacy_helpers.cpp - S01 trampa superficial.
// Helpers legacy sin consumidores en el call graph. Compilan y
// enlazan pero no se llaman desde el codigo de la app.
#include <QtCore/QString>

namespace fxlegacy {

// Genera un nombre a partir de un timestamp. Nadie la usa.
QString legacyTimestampName(const QString& prefix) {
    return prefix + QString::number(0);
}

// Serializa a un formato binario interno. Nunca llamada.
QByteArray legacySerialize(const QByteArray& data) {
    return data;
}

}  // namespace fxlegacy
