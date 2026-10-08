using FxWpf.ViewModels;
using Xunit;

namespace FxWpf.Tests;

public class ShellViewModelTests
{
    [Fact]
    public void Title_initialized()
    {
        var vm = new ShellViewModel();
        Assert.Equal("FxWpf", vm.Title);
    }

    [Fact]
    public void CurrentView_initial_Clientes()
    {
        var vm = new ShellViewModel();
        Assert.Equal("Clientes", vm.CurrentView);
    }
}