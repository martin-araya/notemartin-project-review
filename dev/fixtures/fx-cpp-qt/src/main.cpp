// F06z: main.cpp - entry point de la aplicacion Qt.
#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QQmlApplicationEngine>

#include "qtapp/main_window.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setApplicationName("qtapp");
    app.setOrganizationName("fxemb");

    QQuickStyle::setStyle("Fusion");

    MainWindow w;
    w.show();

    return app.exec();
}
