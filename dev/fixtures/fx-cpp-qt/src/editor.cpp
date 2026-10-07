// F06z: editor.cpp - implementacion de Editor.
//
// E01: connect() entre senales y slots. La skill debe seguir las
// llamadas connect() para entender quien reacciona a que.
#include "qtapp/editor.h"

#include <QFile>
#include <QFileInfo>
#include <QSaveFile>
#include <QTextStream>

Editor::Editor(QObject* parent) : QObject(parent) {}

void Editor::setText(const QString& text) {
    if (m_text == text) return;
    // Guardamos el valor anterior en el stack de undo.
    m_undoStack = m_text;
    m_redoStack.clear();
    m_text = text;
    m_modified = true;
    emit textChanged(m_text);
    emit modificationChanged(true);
}

bool Editor::open(const QString& path) {
    QFile f(path);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) return false;
    m_text = QString::fromUtf8(f.readAll());
    m_currentPath = path;
    m_modified = false;
    emit textChanged(m_text);
    emit modificationChanged(false);
    return true;
}

bool Editor::save(const QString& path) {
    // Escritura atomica: write a .tmp + rename.
    QSaveFile f(path);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) return false;
    f.write(m_text.toUtf8());
    if (!f.commit()) return false;
    m_currentPath = path;
    m_modified = false;
    emit modificationChanged(false);
    return true;
}

void Editor::undo() {
    // Stub: en produccion usariamos QUndoStack.
    if (!m_undoStack.isEmpty()) {
        m_redoStack = m_text;
        m_text = m_undoStack;
        m_undoStack.clear();
        emit textChanged(m_text);
    }
}

void Editor::redo() {
    if (!m_redoStack.isEmpty()) {
        m_undoStack = m_text;
        m_text = m_redoStack;
        m_redoStack.clear();
        emit textChanged(m_text);
    }
}

void Editor::onMarkModified() {
    m_modified = true;
    emit modificationChanged(true);
    // S01: emitimos una senal sin connect receptor.
    emit someUnusedSignal();
}
