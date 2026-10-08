using System.IO;
using Xunit;

namespace FxWpf.TrapTests;

public class TrapPackageTests
{
    private static readonly string FixtureRoot =
        Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));

    [Fact]
    public void P1_onSelectedClienteChanged_no_null_check()
    {
        var vm = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.ViewModels/ClientesViewModel.cs"));
        Assert.Contains("partial void OnSelectedClienteChanged", vm);
        // Trampa: DisplayCliente(newValue) sin null check
        var displayIdx = vm.IndexOf("DisplayCliente(newValue)", System.StringComparison.Ordinal);
        Assert.True(displayIdx >= 0);
        // Debe estar cerca del partial method sin null check previo
        var snippet = vm.Substring(displayIdx, 60);
        Assert.DoesNotContain("if (newValue is null)", snippet);
    }

    [Fact]
    public void P2_SaveCotizacion_uses_TaskRun_without_await()
    {
        var vm = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.ViewModels/CotizacionesViewModel.cs"));
        Assert.Contains("Task.Run", vm);
        // Trampa: Task.Run inside SaveCotizacion method, no awaited.
        var saveIdx = vm.IndexOf("SaveCotizacion", System.StringComparison.Ordinal);
        var body = vm.Substring(saveIdx, 500);
        Assert.Contains("Task.Run", body);
    }

    [Fact]
    public void P3_BoolToVisibilityConverter_ConvertBack_not_implemented()
    {
        var conv = File.ReadAllText(
            Path.Combine(FixtureRoot, "src/FxWpf.App/Converters/BoolToVisibilityConverter.cs"));
        Assert.Contains("ConvertBack", conv);
        // Trampa: throws NotImplementedException
        Assert.Contains("NotImplementedException", conv);
    }

    [Fact]
    public void P4_button_styles_overlap_without_basedon()
    {
        var styles = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/Styles/ButtonStyles.xaml"));
        // 2 Styles que se sobreponen; el ultimo gana.
        Assert.Contains("ButtonStylePrimary", styles);
        Assert.Contains("ButtonStyleOverriding", styles);
        // Trampa: NO usan BasedOn
        Assert.DoesNotContain("BasedOn", styles);
    }

    [Fact]
    public void P5_AsyncRelayCommand_can_execute_returns_false()
    {
        var cmd = File.ReadAllText(
            Path.Combine(FixtureRoot, "src/FxWpf.ViewModels/Commands/AsyncRelayCommand.cs"));
        Assert.Contains("CanExecute", cmd);
        // Trampa: returns false unconditionally
        Assert.Contains("return false", cmd);
    }

    [Fact]
    public void P6_template_datatype_typo()
    {
        var tpl = File.ReadAllText(
            Path.Combine(FixtureRoot, "src/FxWpf.App/Views/Templates/ClienteTemplate.xaml"));
        // Trampa: DataType usa ClientesViewModel cuando deberia ser ClienteViewModel
        Assert.Contains("ClientesViewModel", tpl);
    }
}