using System.IO;
using System.Linq;
using Xunit;

namespace FxWpf.TrapTests;

public class TrapEcosystemTests
{
    private static readonly string FixtureRoot =
        Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));

    [Fact]
    public void E1_xaml_bindings_use_string_path()
    {
        var main = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/Views/MainWindow.xaml"));
        Assert.Contains("{Binding Title}", main);
        Assert.Contains("{Binding Nombre}", main);
        Assert.Contains("{Binding Telefono}", main);
    }

    [Fact]
    public void E2_observable_property_and_relay_command_used()
    {
        var vm = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.ViewModels/ClientesViewModel.cs"));
        Assert.Contains("[ObservableProperty]", vm);
        Assert.Contains("[RelayCommand]", vm);
    }

    [Fact]
    public void E3_data_template_with_datatype_present()
    {
        var template = File.ReadAllText(
            Path.Combine(FixtureRoot, "src/FxWpf.App/Views/Templates/ClienteTemplate.xaml"));
        Assert.Contains("DataTemplate", template);
        Assert.Contains("DataType", template);
    }

    [Fact]
    public void E4_value_converters_exist()
    {
        var convDir = Path.Combine(FixtureRoot, "src/FxWpf.App/Converters");
        Assert.True(File.Exists(Path.Combine(convDir, "BoolToVisibilityConverter.cs")));
        Assert.True(File.Exists(Path.Combine(convDir, "NullToBoolConverter.cs")));
        Assert.True(File.Exists(Path.Combine(convDir, "CurrencyConverter.cs")));
    }

    [Fact]
    public void E5_style_with_triggers_declared()
    {
        var styles = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/Styles/ButtonStyles.xaml"));
        Assert.Contains("<Style.Triggers>", styles);
        Assert.Contains("<DataTrigger", styles);
    }

    [Fact]
    public void E6_app_xaml_has_merged_dictionaries()
    {
        var app = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/App.xaml"));
        Assert.Contains("MergedDictionaries", app);
        Assert.Contains("Themes/Colors.xaml", app);
        Assert.Contains("Themes/Buttons.xaml", app);
        Assert.Contains("Themes/Controls.xaml", app);
    }
}