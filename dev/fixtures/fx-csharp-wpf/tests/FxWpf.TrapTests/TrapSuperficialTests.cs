using System.IO;
using Xunit;

namespace FxWpf.TrapTests;

public class TrapSuperficialTests
{
    private static readonly string FixtureRoot =
        Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));

    [Fact]
    public void S1_LegacyConverter_not_used_in_xaml()
    {
        var conv = File.ReadAllText(
            Path.Combine(FixtureRoot, "src/FxWpf.App/Converters/LegacyConverter.cs"));
        Assert.Contains("LegacyConverter", conv);
        // Search App.xaml + Views for usage
        var appXaml = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/App.xaml"));
        Assert.DoesNotContain("LegacyConverter", appXaml.Replace("LegacyConverter.cs", ""));
    }

    [Fact]
    public void S2_Fonts_xaml_has_unused_FontFamily()
    {
        var fonts = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.App/Themes/Fonts.xaml"));
        Assert.Contains("FontFamily", fonts);
        Assert.Contains("BrandFont", fonts);
        // BrandFont NO esta referenciado en ningun otro XAML.
        foreach (var xamlFile in Directory.GetFiles(Path.Combine(FixtureRoot, "src/FxWpf.App"), "*.xaml", SearchOption.AllDirectories))
        {
            var content = File.ReadAllText(xamlFile);
            // Excluir el propio Fonts.xaml
            if (xamlFile.EndsWith("Fonts.xaml")) continue;
            Assert.DoesNotContain("BrandFont", content);
        }
    }

    [Fact]
    public void S3_ExperimentalViewModel_not_referenced_in_views()
    {
        var vm = File.ReadAllText(Path.Combine(FixtureRoot, "src/FxWpf.ViewModels/ExperimentalViewModel.cs"));
        Assert.Contains("ExperimentalViewModel", vm);
        // No debe ser referenciado en ningun .xaml.cs ni en MainWindow
        foreach (var xamlCs in Directory.GetFiles(Path.Combine(FixtureRoot, "src/FxWpf.App"), "*.xaml.cs", SearchOption.AllDirectories))
        {
            var content = File.ReadAllText(xamlCs);
            Assert.DoesNotContain("ExperimentalViewModel", content);
        }
    }
}