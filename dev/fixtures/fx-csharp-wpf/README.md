# fx-csharp-wpf

Fixture F06ag. App de escritorio WPF con MVVM, bindings XAML por string, source generators de CommunityToolkit.Mvvm (`[ObservableProperty]` + `[RelayCommand]`), `DataTemplate` implícito por `DataType`, value converters, styles con triggers y merged dictionaries en `App.xaml`.

## Stack

- .NET 9.0 (LTS) con SDK `mcr.microsoft.com/dotnet/sdk:9.0`
- WPF con target framework `net9.0-windows` (UI) + `net9.0` (ViewModels + tests)
- CommunityToolkit.Mvvm 8.4.0 con `[ObservableProperty]` + `[RelayCommand]` (source generators)
- XAML nativo con bindings declarativos
- xUnit 2.9.x para tests de ViewModels (cross-platform)

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. Bindings XAML por string de propiedad (`<TextBox Text="{Binding Title, Mode=TwoWay}" />`)
2. Source generators `[ObservableProperty]` + `[RelayCommand]` que emiten código C# parcial
3. `DataTemplate` implícito en `Resources` con `DataType="{x:Type vm:ClienteViewModel}"`
4. Value converters (`IValueConverter`): `BoolToVisibilityConverter`, `NullToBoolConverter`, `CurrencyConverter`
5. Styles con triggers (`<Style.Triggers><DataTrigger Binding="{Binding IsValid}" Value="True">`)
6. Merged dictionaries en `App.xaml` con 3 diccionarios: Colors, Buttons, Controls

### Paquete (P1‑P6)

1. `[ObservableProperty] private Cliente? _clienteSeleccionado` con `partial void OnChanged` sin null check
2. `[RelayCommand] private void SaveCotizacion()` con llamada sincrónica que bloquea la UI
3. `BoolToVisibilityConverter.ConvertBack` que lanza `NotImplementedException`
4. `Style.Triggers` que se sobreponen sin `BasedOn`
5. `ICommand` custom con `CanExecute => false` siempre
6. `DataTemplate.DataType` con typo (no coincide con el VM real)

### Superficiales (S1‑S3)

1. `Converters/LegacyConverter.cs` con `Convert` declarado pero no invocado
2. `Themes/Fonts.xaml` con `<FontFamily>` declarado pero no referenciado
3. `ViewModels/ExperimentalViewModel.cs` declarado pero no usado

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `clientes` | 7 (R-01..R-07) | E1, E2, E3, E4, P1, P3, R-07 deep link |
| `cotizaciones` | 7 (R-01..R-07) | E1, E2, E5, P2, P4, R-04 currency converter |
| `impresión` | 7 (R-01..R-07) | E1, E4, R-05 cadena, R-07 deep link |

## Cómo correr

### Tests de ViewModels (cross-platform)

```bash
cd dev/fixtures/fx-csharp-wpf
dotnet test --logger "console;verbosity=normal"
```

### En contenedor CI

```bash
docker build -f dev/fixtures/fx-csharp-wpf/Dockerfile.test -t npr-fx-csharp-wpf dev/fixtures/fx-csharp-wpf/
docker run --rm -v $(pwd)/dev/fixtures/fx-csharp-wpf/.nuget-cache:$(HOME)/.nuget/packages npr-fx-csharp-wpf
```

### Tests de UI WPF (Windows only)

Los tests con `[Trait("Category", "UI")]` requieren Windows con .NET 9 SDK + WPF runtime. Se omiten en Linux/macOS CI.

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-csharp-wpf --container
```

## Limitación documentada

**La UI de WPF solo se puede testear en Windows.** Los tests de **ViewModels** corren multiplataforma (Linux/macOS/Windows) gracias a que los ViewModels son `net9.0` puro sin dependencias de WPF. Los tests de UI están marcados con `[Trait("Category", "UI")]` y se omiten automáticamente en CI Linux.