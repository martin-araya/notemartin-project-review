# Signal/Slot cheatsheet — F06z

## Patrones de conexion en Qt 6

1. **connect explicito** (E01): `QObject::connect(sender, signal, receiver, slot)`.
2. **Lambda connect**: `QObject::connect(sender, &S::sig, this, [this](args){...});`.
3. **Auto-connect** (E02): slot con nombre `on_<objectName>_<signal>` se conecta automaticamente cuando se llama a `setupUi()`.
4. **Q_INVOKABLE** (E04): metodo callable desde QML.
5. **Q_PROPERTY** (E04): propiedad observable desde QML si tiene `NOTIFY`.

## Trampas comunes

- `connect_5_args_no_explicit` (P01): la quinta posicion es el contexto (thread); pasarla mal causa UB.
- `signal_loop_infinite` (P02): un slot que emite la misma senal que lo dispara.
- `q_property_no_notify` (P03): `Q_PROPERTY` sin `NOTIFY` no actualiza los bindings de QML.
- `qrc_path_no_colon_slash` (P04): la ruta debe empezar con `:/` (e.g. `:/icons/save.svg`).
- `auto_connect_name_typo` (P05): `on_savebutton_clicked` no se autoconnecta si el objectName es `saveButton` (con mayuscula).
- `qml_garbage_collected` (P06): un QObject* expuesto a QML sin `setObjectOwnership(..., CppOwnership)` puede ser borrado por el GC.

## Mejores practicas

- Usar `Q_OBJECT` macro en cualquier clase con senales/slots/properties.
- Preferir `QObject::connect` con punteros a miembro (`&Class::method`) sobre strings (`SIGNAL(...)`).
- Para QML, preferir `Q_PROPERTY` con `NOTIFY` sobre getters/setters publicos.
- Usar `qt_add_qml_module` para registrar QML con su URI.
- Para tests, usar `QT_QPA_PLATFORM=offscreen` en CI sin display.
