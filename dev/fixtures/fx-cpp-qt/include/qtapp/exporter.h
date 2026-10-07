// F06z: exporter.h - QObject con Q_INVOKABLE para exportar texto.
//
// E04: Q_INVOKABLE permite llamar estas funciones desde QML. La
// trampaa E01 (connect) tambien vive aqui: emitimos exportCompleted
// al terminar, que MainWindow conecta al status bar.
#pragma once

#include <QObject>
#include <QString>

class Exporter : public QObject {
    Q_OBJECT
public:
    explicit Exporter(QObject* parent = nullptr);

    // API imperativa.
    bool exportToText(const QString& path, const QString& content);
    bool exportToHtml(const QString& path, const QString& content);
    bool exportToMarkdown(const QString& path, const QString& content);

    // E04: Q_INVOKABLE para QML.
    Q_INVOKABLE bool exportFile(const QString& path, const QString& content, const QString& format);

    // E01: senal que MainWindow conecta al status bar.
signals:
    void exportCompleted(const QString& path, bool success);
    void exportFailed(const QString& path, const QString& reason);

public slots:
    void doExport(const QString& path, const QString& content, const QString& format);
};
