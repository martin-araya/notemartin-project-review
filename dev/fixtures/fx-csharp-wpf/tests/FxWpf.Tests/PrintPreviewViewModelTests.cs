using FxWpf.ViewModels;
using Xunit;

namespace FxWpf.Tests;

public class PrintPreviewViewModelTests
{
    [Fact]
    public void DocumentPath_initial_empty()
    {
        var vm = new PrintPreviewViewModel();
        Assert.Equal(string.Empty, vm.DocumentPath);
    }

    [Fact]
    public void Status_initial_is_Listo()
    {
        var vm = new PrintPreviewViewModel();
        Assert.Equal("Listo", vm.Status);
    }

    [Fact]
    public void IsValid_initial_true()
    {
        var vm = new PrintPreviewViewModel();
        Assert.True(vm.IsValid);
    }
}