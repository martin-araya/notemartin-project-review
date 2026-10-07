// F06z: main_window.h - QWidget con setupUi() desde main_window.ui.
//
// E02: auto-conexion. Los slots con la convencion
// `on_<objectName>_<signal>` se conectan automaticamente por Qt a
// los signals de los widgets con el objectName correspondiente.
// E01: connect explicito para Editor::textChanged y Exporter::exportCompleted.
#pragma once

#include <QMainWindow>

QT_BEGIN_NAMESPACE
class QAction;
class QMenu;
class QPlainTextEdit;
class Ui_MainWindow;  // E03: generado por uic desde ui/main_window.ui
class Editor;
class Exporter;
class Preferences;
class PreferencesProxy;
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit MainWindow(QWidget* parent = nullptr);
    ~MainWindow() override;

    Editor* editor() const { return m_editor; }
    Exporter* exporter() const { return m_exporter; }
    Preferences* preferences() const { return m_preferences; }
    PreferencesProxy* preferencesProxy() const { return m_preferencesProxy; }

public slots:
    // E02: auto-connect slots. Los objectNames de los widgets en
    // main_window.ui deben llamarse saveButton, exitButton,
    // exportButton, preferencesButton.
    void on_saveButton_clicked();
    void on_exitButton_clicked();
    void on_exportButton_clicked();
    void on_preferencesButton_clicked();

    // P05 trampa paquete: slot con typo en el nombre. La auto-conexion
    // falla silenciosamente y la skill debe notar la discrepancia.
    void on_savebutton_clicked_TYPO();

    void on_textEdit_textChanged();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionExport_triggered();
    void on_actionPreferences_triggered();
    void on_actionQuit_triggered();

private:
    void setupConnections();

    Ui_MainWindow* ui = nullptr;  // E03: objeto generado por uic
    Editor* m_editor = nullptr;
    Exporter* m_exporter = nullptr;
    Preferences* m_preferences = nullptr;
    PreferencesProxy* m_preferencesProxy = nullptr;
    QPlainTextEdit* m_textEdit = nullptr;
    QAction* m_actionOpen = nullptr;
    QAction* m_actionSave = nullptr;
    QAction* m_actionExport = nullptr;
    QAction* m_actionPreferences = nullptr;
    QAction* m_actionQuit = nullptr;
};
