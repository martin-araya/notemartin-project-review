# Ground truth — fx-csharp-wpf (F06ag)

Fixture WPF con .NET 9, MVVM via CommunityToolkit.Mvvm, bindings XAML por string, source generators `[ObservableProperty]` + `[RelayCommand]`, `DataTemplate` implícito por `DataType`, value converters, styles con triggers y merged dictionaries en `App.xaml`. Ver `ground_truth.json` para la maquina y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | .NET 9.0 + WPF (net9.0-windows) + CommunityToolkit.Mvvm 8.4.0 + xUnit 2.9.2 |
| Plataforma | Windows (UI) + Linux/macOS (tests ViewModels) |
| Features | 3: clientes, cotizaciones, impresión |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 13 (4 screens + 1 data-template + 3 converters + 1 style + 3 resource-dictionaries + 2 commands) |
| Unique tokens | 34 con prefijo `NPRGT-FXWPF-` |

## Trampas del ecosistema

1. **TRAP-E1 — xaml_bindings_string_path** (`MainWindow.xaml:13`): 5+ bindings por string.
2. **TRAP-E2 — mvvm_source_generators** (`ClientesViewModel.cs:36`): `[ObservableProperty]` + `[RelayCommand]`.
3. **TRAP-E3 — data_template_with_datatype** (`ClienteTemplate.xaml:7`): `DataType="{x:Type vm:ClienteViewModel}"`.
4. **TRAP-E4 — value_converters** (`BoolToVisibilityConverter.cs:8`): 3 `IValueConverter`.
5. **TRAP-E5 — style_triggers** (`ButtonStyles.xaml:11`): `Style.Triggers` con `DataTrigger`.
6. **TRAP-E6 — merged_dictionaries** (`App.xaml:11`): 4 `MergedDictionaries`.

## Trampas del paquete

1. **TRAP-P1 — on_selected_changed_no_null_check** (`ClientesViewModel.cs:42`): sin null check.
2. **TRAP-P2 — save_cotizacion_task_run_no_await** (`CotizacionesViewModel.cs:39`): `Task.Run` sin `await`.
3. **TRAP-P3 — converter_convert_back_not_impl** (`BoolToVisibilityConverter.cs:25`): throw `NotImplementedException`.
4. **TRAP-P4 — style_overlapping_no_basedon** (`ButtonStyles.xaml:13`): 2 styles sin `BasedOn`.
5. **TRAP-P5 — async_relay_command_never_enabled** (`AsyncRelayCommand.cs:24`): `CanExecute => false` siempre.
6. **TRAP-P6 — template_datatype_typo** (`ClienteTemplate.xaml:7`): `DataType={x:Type vm:ClientesViewModel}` typo.

## Trampas superficiales

1. **TRAP-S1 — legacy_converter_unused** (`LegacyConverter.cs:9`).
2. **TRAP-S2 — fonts_xaml_unused** (`Fonts.xaml:5`).
3. **TRAP-S3 — experimental_viewmodel_unused** (`ExperimentalViewModel.cs:6`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitación operativa

**La UI de WPF solo se puede testear en Windows.** Los tests de **ViewModels** corren multiplataforma (Linux/macOS/Windows) gracias a que los ViewModels son `net9.0` puro sin dependencias de WPF. Los tests de UI están marcados con `[Trait("Category", "UI")]` y se omiten automáticamente en CI Linux.