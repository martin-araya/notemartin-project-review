// F06z: main_window.cpp - implementacion de MainWindow.
//
// E02: auto-conexion. El constructor llama setupUi() que conecta
// automaticamente los slots con la convencion on_<objectName>_<signal>
// a las senales de los widgets en main_window.ui.
//
// E01: connect explicito para Editor::textChanged y
// Exporter::exportCompleted.
#include "qtapp/main_window.h"
#include "qtapp/editor.h"
#include "qtapp/exporter.h"
#include "qtapp/preferences.h"
#include "qtapp/preferences_proxy.h"

#include <QFileDialog>
#include <QMenuBar>
#include <QMessageBox>
#include <QPlainTextEdit>
#include <QStatusBar>
#include <QToolBar>

#include "ui_main_window.h"

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent),
      ui(new Ui_MainWindow),
    m_editor(new Editor(this)),
    m_exporter(new Exporter(this)),
    m_preferences(new Preferences(this)),
    m_preferencesProxy(new PreferencesProxy(m_preferences, this)) {
    ui->setupUi(this);
    m_textEdit = ui->textEdit;

    setupConnections();

    m_preferences->load();
    QFont f = m_textEdit->font();
    f.setPointSize(m_preferences->fontSize());
    m_textEdit->setFont(f);

    setWindowTitle("fxproc Qt App");
    statusBar()->showMessage("Listo", 2000);
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::setupConnections() {
    // E01: connect explicito entre senales y slots.
    // P01 trampa paquete: connect_5_args_no_explicit. La firma
    // habitual de connect es (sender, signal, receiver, slot). La
    // quinta posicion es el contexto (thread). Pasarla mal causa
    // UB en threads. La firma correcta es 4 argumentos.
    QObject::connect(m_editor, &Editor::textChanged,
                     m_textEdit, &QPlainTextEdit::setPlainText);
    QObject::connect(m_textEdit, &QPlainTextEdit::textChanged,
                     m_editor, &Editor::onMarkModified);
    QObject::connect(m_editor, &Editor::textChanged,
                     this, [this](const QString&) {
                         statusBar()->showMessage(
                             QString("Caracteres: %1").arg(m_textEdit->toPlainText().length()),
                             2000);
                     });
    QObject::connect(m_exporter, &Exporter::exportCompleted,
                     this, [this](const QString& path, bool ok) {
                         statusBar()->showMessage(
                             ok ? QString("Exportado a %1").arg(path)
                                : "Error al exportar",
                             3000);
                     });
    QObject::connect(m_preferences, &Preferences::darkThemeChanged,
                     this, [this](bool enabled) {
                         if (enabled) {
                             qApp->setStyleSheet("QWidget { background: #2b2b2b; color: #eee; }");
                         } else {
                             qApp->setStyleSheet("");
                         }
                     });
}

// --- Auto-connect slots (E02) ---

void MainWindow::on_saveButton_clicked() {
    QString path = QFileDialog::getSaveFileName(this, "Guardar", QString(), "Todos (*)");
    if (path.isEmpty()) return;
    QString content = m_textEdit->toPlainText();
    if (m_editor->save(path)) {
        statusBar()->showMessage("Guardado en " + path, 3000);
    } else {
        QMessageBox::warning(this, "Error", "No se pudo guardar el archivo");
    }
}

void MainWindow::on_exitButton_clicked() {
    close();
}

void MainWindow::on_exportButton_clicked() {
    QString path = QFileDialog::getSaveFileName(this, "Exportar", QString(), "Texto (*.txt);;HTML (*.html);;Markdown (*.md)");
    if (path.isEmpty()) return;
    QString format = "text";
    if (path.endsWith(".html", Qt::CaseInsensitive)) format = "html";
    else if (path.endsWith(".md", Qt::CaseInsensitive)) format = "md";
    m_exporter->doExport(path, m_textEdit->toPlainText(), format);
}

void MainWindow::on_preferencesButton_clicked() {
    QMessageBox::information(this, "Preferencias",
        QString("Font: %1\nTema oscuro: %2").arg(m_preferences->fontSize()).arg(m_preferences->darkTheme() ? "si" : "no"));
}

void MainWindow::on_savebutton_clicked_TYPO() {
    // P05 trampa paquete: auto_connect_name_typo. El nombre del
    // slot no coincide con la convencion on_<objectName>_<signal>
    // porque el objectName es "saveButton" (capital B) y el slot
    // empieza con minuscula. La auto-conexion falla silenciosamente.
    statusBar()->showMessage("typo slot llamado", 1000);
}

void MainWindow::on_textEdit_textChanged() {
    m_editor->setText(m_textEdit->toPlainText());
}

void MainWindow::on_actionOpen_triggered() {
    QString path = QFileDialog::getOpenFileName(this, "Abrir", QString(), "Todos (*)");
    if (path.isEmpty()) return;
    if (m_editor->open(path)) {
        m_textEdit->setPlainText(m_editor->text());
    }
}

void MainWindow::on_actionSave_triggered() {
    on_saveButton_clicked();
}

void MainWindow::on_actionExport_triggered() {
    on_exportButton_clicked();
}

void MainWindow::on_actionPreferences_triggered() {
    on_preferencesButton_clicked();
}

void MainWindow::on_actionQuit_triggered() {
    // S03 trampa superficial: commented_out_connect. Las siguientes
    // 3 lineas son codigo comentado que parece activo. La trampa es
    // que la skill puede pensar que esta conectado.
    //   TODO: connect to undoStack
    //   TODO: connect to on_actionSave_triggered
    //   TODO: connect to preferencesChanged
    close();
}
