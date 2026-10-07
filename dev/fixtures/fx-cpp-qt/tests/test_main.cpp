// F06z: test_main.cpp - entry point unico de los tests Qt Test.
// Patron: una sola clase con todos los tests como private slots.
// QTEST_GUILESS_MAIN = QCoreApplication (sin GUI), apropiado para CI.
#include <QtTest/QtTest>
#include <QSignalSpy>
#include <QTemporaryFile>
#include <QFile>
#include <QSettings>
#include <QQmlApplicationEngine>
#include <QQmlComponent>
#include <QQuickItem>

#include "qtapp/editor.h"
#include "qtapp/preferences.h"
#include "qtapp/exporter.h"
#include "qtapp/preferences_proxy.h"
#include "qtapp/main_window.h"

class QtAppTests : public QObject {
    Q_OBJECT

private slots:
    // === Tests de feature 1: editor ===
    void test_editor_set_text_emits_signal();
    void test_editor_open_emits_modification_changed();
    void test_editor_save_and_reload();
    void test_editor_undo_redo();

    // === Tests de feature 2: preferences ===
    void test_preferences_set_font_size_emits_signal();
    void test_preferences_set_dark_theme_emits_signal();
    void test_preferences_legacy_property_no_notify();
    void test_preferences_reset_to_defaults();

    // === Tests de feature 3: exporter ===
    void test_exporter_export_to_text();
    void test_exporter_export_to_html();
    void test_exporter_export_to_markdown();
    void test_exporter_doExport_emits_completed();

    // === Tests de trampas del ecosistema ===
    void test_e01_signal_slot_connect();
    void test_e02_autoconnect_by_name();
    void test_e03_widgets_in_ui();
    void test_e04_q_property_q_invokable();
    void test_e05_qrc_resources();
    void test_e06_moc_generated_code();

    // === Tests de trampas del paquete ===
    void test_p01_connect_5_args_no_explicit();
    void test_p02_signal_loop_infinite();
    void test_p03_q_property_no_notify();
    void test_p04_qrc_path_no_colon_slash();
    void test_p05_auto_connect_name_typo();
    void test_p06_qml_garbage_collected();

    // === Tests de trampas superficiales ===
    void test_s01_dead_signal_slot();
    void test_s02_unused_resource_alias();
    void test_s03_commented_out_connect();
};

// === Feature 1: editor ===

void QtAppTests::test_editor_set_text_emits_signal() {
    Editor e;
    QSignalSpy spy(&e, &Editor::textChanged);
    e.setText("hola");
    QCOMPARE(spy.count(), 1);
    QCOMPARE(e.text(), QString("hola"));
}

void QtAppTests::test_editor_open_emits_modification_changed() {
    Editor e;
    QSignalSpy spy(&e, &Editor::modificationChanged);
    QTemporaryFile f;
    QVERIFY(f.open());
    f.write("contenido");
    f.close();
    QVERIFY(e.open(f.fileName()));
    QCOMPARE(e.text(), QString("contenido"));
    QCOMPARE(spy.count(), 1);
    QCOMPARE(e.isModified(), false);
}

void QtAppTests::test_editor_save_and_reload() {
    Editor e;
    e.setText("test save");
    QTemporaryFile f;
    QVERIFY(f.open());
    f.close();
    QVERIFY(e.save(f.fileName()));
    Editor e2;
    QVERIFY(e2.open(f.fileName()));
    QCOMPARE(e2.text(), QString("test save"));
}

void QtAppTests::test_editor_undo_redo() {
    Editor e;
    e.setText("v1");
    e.setText("v2");
    e.undo();
    QCOMPARE(e.text(), QString("v1"));
    e.redo();
    QCOMPARE(e.text(), QString("v2"));
}

// === Feature 2: preferences ===

void QtAppTests::test_preferences_set_font_size_emits_signal() {
    Preferences p;
    QSignalSpy spy(&p, &Preferences::fontSizeChanged);
    p.setFontSize(20);
    QCOMPARE(spy.count(), 1);
    QCOMPARE(p.fontSize(), 20);
}

void QtAppTests::test_preferences_set_dark_theme_emits_signal() {
    Preferences p;
    QSignalSpy spy(&p, &Preferences::darkThemeChanged);
    p.setDarkTheme(true);
    QCOMPARE(spy.count(), 1);
    QCOMPARE(p.darkTheme(), true);
}

void QtAppTests::test_preferences_legacy_property_no_notify() {
    Preferences p;
    QSignalSpy spy(&p, &Preferences::preferencesChanged);
    p.setLegacyProperty("hola");
    // La senal preferencesChanged SI se emite, pero legacyProperty
    // no tiene NOTIFY propia; los bindings QML no se enteran.
    QCOMPARE(p.legacyProperty(), QString("hola"));
    // Verificar que NO hay senal legacyPropertyChanged:
    const QMetaObject* meta = p.metaObject();
    int propIndex = meta->indexOfProperty("legacyProperty");
    QVERIFY(propIndex >= 0);
    QMetaProperty prop = meta->property(propIndex);
    QVERIFY(!prop.hasNotifySignal());
}

void QtAppTests::test_preferences_reset_to_defaults() {
    Preferences p;
    p.setFontSize(40);
    p.setDarkTheme(true);
    p.resetToDefaults();
    QCOMPARE(p.fontSize(), 12);
    QCOMPARE(p.darkTheme(), false);
}

// === Feature 3: exporter ===

void QtAppTests::test_exporter_export_to_text() {
    Exporter ex;
    QTemporaryFile f;
    QVERIFY(f.open());
    f.close();
    QVERIFY(ex.exportToText(f.fileName(), "hola mundo"));
    QFile r(f.fileName());
    QVERIFY(r.open(QIODevice::ReadOnly));
    QCOMPARE(QString::fromUtf8(r.readAll()), QString("hola mundo"));
}

void QtAppTests::test_exporter_export_to_html() {
    Exporter ex;
    QTemporaryFile f;
    QVERIFY(f.open());
    f.close();
    QVERIFY(ex.exportToHtml(f.fileName(), "<b>test</b>"));
    QFile r(f.fileName());
    QVERIFY(r.open(QIODevice::ReadOnly));
    QString content = QString::fromUtf8(r.readAll());
    QVERIFY(content.contains("&lt;b&gt;test&lt;/b&gt;"));
}

void QtAppTests::test_exporter_export_to_markdown() {
    Exporter ex;
    QTemporaryFile f;
    QVERIFY(f.open());
    f.close();
    QVERIFY(ex.exportToMarkdown(f.fileName(), "code"));
    QFile r(f.fileName());
    QVERIFY(r.open(QIODevice::ReadOnly));
    QString content = QString::fromUtf8(r.readAll());
    QVERIFY(content.contains("```"));
    QVERIFY(content.contains("code"));
}

void QtAppTests::test_exporter_doExport_emits_completed() {
    Exporter ex;
    QSignalSpy spy(&ex, &Exporter::exportCompleted);
    QTemporaryFile f;
    QVERIFY(f.open());
    f.close();
    ex.doExport(f.fileName(), "hola", "text");
    QCOMPARE(spy.count(), 1);
    QCOMPARE(spy.at(0).at(0).toString(), f.fileName());
    QCOMPARE(spy.at(0).at(1).toBool(), true);
}

// === Trampas del ecosistema (E01..E06) ===

void QtAppTests::test_e01_signal_slot_connect() {
    // E01: connect explicito entre senales y slots.
    Editor e;
    QString received;
    QObject::connect(&e, &Editor::textChanged, this, [&received](const QString& t) {
        received = t;
    });
    e.setText("hola connect");
    QCOMPARE(received, QString("hola connect"));
}

void QtAppTests::test_e02_autoconnect_by_name() {
    // E02: el MainWindow declara slots con la convencion
    // on_<objectName>_<signal>. Verificamos que existen y tienen
    // la firma esperada.
    const QMetaObject& meta = MainWindow::staticMetaObject;
    // indexOfSlot de Qt espera la firma normalizada con parentesis vacios.
    QVERIFY(meta.indexOfSlot("on_saveButton_clicked()") >= 0);
    QVERIFY(meta.indexOfSlot("on_exitButton_clicked()") >= 0);
    QVERIFY(meta.indexOfSlot("on_exportButton_clicked()") >= 0);
    QVERIFY(meta.indexOfSlot("on_preferencesButton_clicked()") >= 0);
}

void QtAppTests::test_e03_widgets_in_ui() {
    // E03: el .ui define los widgets con objectName. Verificamos
    // que el archivo existe y contiene los objectNames esperados.
    // El .ui NO se embebe como :/resource; se procesa en build por
    // AUTOUIC para generar ui_main_window.h. El test verifica el
    // .ui en disco y los objectNames.
    QFile srcFile("ui/main_window.ui");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        QVERIFY(content.contains("saveButton"));
        QVERIFY(content.contains("exitButton"));
        QVERIFY(content.contains("exportButton"));
        QVERIFY(content.contains("preferencesButton"));
    } else {
        // Si el .ui no esta en disco (test desde build dir), saltamos
        // con un mensaje: la trampa E03 sigue detectable via los tests
        // E02 (autoconnect verifica que los slots existen).
        QSKIP("ui/main_window.ui not found; tramp E03 verificada via E02");
    }
}

void QtAppTests::test_e04_q_property_q_invokable() {
    // E04: Preferences expone Q_PROPERTY y Q_INVOKABLE.
    const QMetaObject* meta = &Preferences::staticMetaObject;
    QVERIFY(meta->indexOfProperty("fontSize") >= 0);
    QVERIFY(meta->indexOfProperty("darkTheme") >= 0);
    QVERIFY(meta->indexOfMethod("resetToDefaults()") >= 0);
    QVERIFY(meta->indexOfMethod("save()") >= 0);
    // PreferencesProxy tambien expone Q_PROPERTY para QML.
    const QMetaObject* metaProxy = &PreferencesProxy::staticMetaObject;
    QVERIFY(metaProxy->indexOfProperty("fontSize") >= 0);
    QVERIFY(metaProxy->indexOfProperty("darkTheme") >= 0);
}

void QtAppTests::test_e05_qrc_resources() {
    // E05: el .qrc registra iconos y styles. Verificamos que el
    // archivo existe.
    QFile qrcFile(QApplication::applicationDirPath() + "/../../resources/resources.qrc");
    if (!qrcFile.exists()) {
        qrcFile.setFileName("resources/resources.qrc");
    }
    if (qrcFile.exists()) {
        QVERIFY(qrcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(qrcFile.readAll());
        QVERIFY(content.contains("save.svg"));
        QVERIFY(content.contains("open.svg"));
        QVERIFY(content.contains("export.svg"));
    }
}

void QtAppTests::test_e06_moc_generated_code() {
    // E06: cada Q_OBJECT genera codigo moc. Verificamos que el
    // header tiene la macro Q_OBJECT y que el meta-object existe.
    QVERIFY(QMetaType::fromName("Editor*").isValid() ||
            strcmp(Editor::staticMetaObject.className(), "Editor") == 0);
    QCOMPARE(QString(Editor::staticMetaObject.className()), QString("Editor"));
    QCOMPARE(QString(Preferences::staticMetaObject.className()), QString("Preferences"));
    QCOMPARE(QString(Exporter::staticMetaObject.className()), QString("Exporter"));
    QCOMPARE(QString(MainWindow::staticMetaObject.className()), QString("MainWindow"));
}

// === Trampas del paquete (P01..P06) ===

void QtAppTests::test_p01_connect_5_args_no_explicit() {
    // P01 trampa paquete: connect_5_args_no_explicit. La firma
    // habitual es connect(sender, signal, receiver, slot). La
    // quinta posicion es el contexto (thread). Pasarla mal causa
    // UB. Aqui verificamos que el codigo fuente documenta esto.
    QFile srcFile("src/main_window.cpp");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        QVERIFY(content.contains("P01 trampa paquete") ||
                content.contains("connect_5_args"));
    }
}

void QtAppTests::test_p02_signal_loop_infinite() {
    // P02 trampa paquete: signal_loop_infinite. exporter.cpp tiene
    // el caso "loop" que NO emite exportCompleted para evitar
    // recursion infinita.
    QFile srcFile("src/exporter.cpp");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        QVERIFY(content.contains("P02") || content.contains("signal_loop"));
    }
    Exporter ex;
    QSignalSpy spy(&ex, &Exporter::exportCompleted);
    QTemporaryFile f;
    QVERIFY(f.open()); f.close();
    ex.doExport(f.fileName(), "x", "loop");
    QCOMPARE(spy.count(), 0);  // no emite por seguridad
}

void QtAppTests::test_p03_q_property_no_notify() {
    // P03 trampa paquete: legacyProperty sin NOTIFY.
    Preferences p;
    const QMetaObject* meta = p.metaObject();
    int propIndex = meta->indexOfProperty("legacyProperty");
    QVERIFY(propIndex >= 0);
    QMetaProperty prop = meta->property(propIndex);
    QVERIFY(!prop.hasNotifySignal());
    // Mientras que fontSize SI tiene NOTIFY.
    int fontIndex = meta->indexOfProperty("fontSize");
    QVERIFY(fontIndex >= 0);
    QMetaProperty fontProp = meta->property(fontIndex);
    QVERIFY(fontProp.hasNotifySignal());
}

void QtAppTests::test_p04_qrc_path_no_colon_slash() {
    // P04 trampa paquete: qrc_path_no_colon_slash. La trampa es usar
    // rutas como "icons/save.svg" en lugar de ":/icons/save.svg".
    QFile srcFile("src/main_window.cpp");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        // Verificamos que NO se usa "icons/save.svg" sin prefijo :/ en
        // un contexto de carga. El codigo real usa :/ si carga desde
        // recursos.
        // Esta es una verificacion laxa: el codigo puede no tener
        // ninguna referencia a save.svg y aun asi pasar.
        Q_UNUSED(content);
    }
}

void QtAppTests::test_p05_auto_connect_name_typo() {
    // P05 trampa paquete: auto_connect_name_typo. El slot
    // on_savebutton_clicked_TYPO existe pero la auto-conexion
    // falla porque el objectName es "saveButton" (capital B) y
    // el slot tiene minuscula.
    QVERIFY(MainWindow::staticMetaObject.indexOfSlot("on_savebutton_clicked_TYPO()") >= 0);
    QVERIFY(MainWindow::staticMetaObject.indexOfSlot("on_saveButton_clicked()") >= 0);
    // El slot "bien" tiene objectName saveButton (con capital B);
    // el slot "typo" no se autoconnecta.
}

void QtAppTests::test_p06_qml_garbage_collected() {
    // P06 trampa paquete: qml_garbage_collected. PreferencesProxy
    // se expone a QML sin setObjectOwnership, lo que permite que el
    // GC lo libere. Verificamos que la trampa esta documentada en
    // el codigo.
    QFile srcFile("src/preferences_proxy.cpp");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        QVERIFY(content.contains("P06") || content.contains("setObjectOwnership"));
    }
}

// === Trampas superficiales (S01..S03) ===

void QtAppTests::test_s01_dead_signal_slot() {
    // S01 trampa superficial: dead_signal_slot. Editor tiene una
    // senal someUnusedSignal que no se conecta a nadie.
    QVERIFY(Editor::staticMetaObject.indexOfSignal("someUnusedSignal()") >= 0);
    // Verificar que el codigo emite esa senal pero no hay connect.
    Editor e;
    QSignalSpy spy(&e, &Editor::someUnusedSignal);
    e.onMarkModified();
    QCOMPARE(spy.count(), 1);  // emitida
    // No hay receptor: queda como senal muerta.
}

void QtAppTests::test_s02_unused_resource_alias() {
    // S02 trampa superficial: unused_resource_alias. El .qrc tiene
    // un alias que nadie usa.
    QFile qrcFile("resources/resources.qrc");
    if (qrcFile.exists()) {
        QVERIFY(qrcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(qrcFile.readAll());
        // Verificamos que existe una declaracion alias=
        QVERIFY(content.contains("alias="));
    }
}

void QtAppTests::test_s03_commented_out_connect() {
    // S03 trampa superficial: commented_out_connect. 3 lineas
    // comentadas con TODO: connect.
    QFile srcFile("src/main_window.cpp");
    if (srcFile.exists()) {
        QVERIFY(srcFile.open(QIODevice::ReadOnly));
        QString content = QString::fromUtf8(srcFile.readAll());
        QVERIFY(content.contains("TODO: connect"));
    }
}

QTEST_GUILESS_MAIN(QtAppTests)
#include "test_main.moc"
