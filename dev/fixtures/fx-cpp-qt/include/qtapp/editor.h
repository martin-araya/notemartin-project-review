// F06z: editor.h - QObject con signals y slots (trampa E01 del ecosistema).
//
// E01: connect() entre senales y slots es una llamada indirecta. La
// skill debe seguir el connect() en editor.cpp para entender quien
// reacciona a que.
#pragma once

#include <QObject>
#include <QString>

class Editor : public QObject {
    Q_OBJECT
public:
    explicit Editor(QObject* parent = nullptr);

    // API.
    void setText(const QString& text);
    QString text() const { return m_text; }
    bool isModified() const { return m_modified; }
    bool open(const QString& path);
    bool save(const QString& path);

    void undo();
    void redo();

public slots:
    // S03: dead_signal_slot. El slot esta pero no se usa.
    void onMarkModified();

signals:
    // E01: senales que se conectan a slots en otras partes.
    void textChanged(const QString& newText);
    void modificationChanged(bool modified);
    // S01: senal declarada y emitida en algun lugar pero sin connect.
    void someUnusedSignal();

private:
    QString m_text;
    bool m_modified = false;
    QString m_currentPath;
    // Stubs simples de historial (en produccion usariamos QUndoStack).
    QString m_undoStack;
    QString m_redoStack;
};
