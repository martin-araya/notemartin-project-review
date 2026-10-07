// F06z: exporter.cpp - implementacion de Exporter.
#include "qtapp/exporter.h"

#include <QFile>
#include <QFileInfo>
#include <QTextStream>
#include <QSaveFile>

Exporter::Exporter(QObject* parent) : QObject(parent) {}

bool Exporter::exportToText(const QString& path, const QString& content) {
    QFile f(path);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) return false;
    f.write(content.toUtf8());
    emit exportCompleted(path, true);
    return true;
}

bool Exporter::exportToHtml(const QString& path, const QString& content) {
    // Envolvemos en HTML basico.
    QString html = "<html><body><pre>" + content.toHtmlEscaped() + "</pre></body></html>";
    QFile f(path);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) return false;
    f.write(html.toUtf8());
    emit exportCompleted(path, true);
    return true;
}

bool Exporter::exportToMarkdown(const QString& path, const QString& content) {
    QString md = "# Export\n\n```\n" + content + "\n```\n";
    QFile f(path);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) return false;
    f.write(md.toUtf8());
    emit exportCompleted(path, true);
    return true;
}

bool Exporter::exportFile(const QString& path, const QString& content, const QString& format) {
    if (format == "text") return exportToText(path, content);
    if (format == "html") return exportToHtml(path, content);
    if (format == "md") return exportToMarkdown(path, content);
    return false;
}

void Exporter::doExport(const QString& path, const QString& content, const QString& format) {
    // P02 trampa paquete: signal_loop_infinite. Si exportamos con
    // formato "loop", el codigo emite exportCompleted que main_window
    // conecta a onExportButton_clicked que llama a doExport otra vez.
    // En produccion esto causa recursion infinita. En este stub
    // simplemente no emitimos nada (la trampa queda documentada en
    // el comment).
    if (format == "loop") {
        // NO emitimos exportCompleted para evitar el loop.
        return;
    }
    if (!exportFile(path, content, format)) {
        emit exportFailed(path, "cannot write to file");
    }
}
