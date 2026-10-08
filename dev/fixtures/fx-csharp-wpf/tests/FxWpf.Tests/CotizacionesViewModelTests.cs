using FxWpf.ViewModels;
using Xunit;

namespace FxWpf.Tests;

public class CotizacionesViewModelTests
{
    [Fact]
    public void Title_initialized()
    {
        var vm = new CotizacionesViewModel();
        Assert.Equal("Cotizaciones", vm.Title);
    }

    [Fact]
    public void Cotizaciones_initial_list_not_empty()
    {
        var vm = new CotizacionesViewModel();
        Assert.NotEmpty(vm.Cotizaciones);
    }

    [Fact]
    public void AddCotizacion_can_execute_when_moneda_set()
    {
        var vm = new CotizacionesViewModel
        {
            Moneda = "USD",
        };
        Assert.True(vm.AddCotizacionCommand.CanExecute(null));
    }

    [Fact]
    public void Moneda_initial_is_USD()
    {
        var vm = new CotizacionesViewModel();
        Assert.Equal("USD", vm.Moneda);
    }
}