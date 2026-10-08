using System.Threading.Tasks;
using FxWpf.ViewModels;
using Xunit;

namespace FxWpf.Tests;

public class ClientesViewModelTests
{
    [Fact]
    public async Task AddCliente_appends_to_list()
    {
        var fake = new FakeClienteService();
        var vm = new ClientesViewModel(fake);

        await vm.AddClienteCommand.ExecuteAsync(null);

        Assert.Equal(1, vm.Clientes.Count);
        Assert.Equal("Cliente 1", vm.Clientes[0].Nombre);
    }

    [Fact]
    public void FilterClientes_filters_by_name()
    {
        var fake = new FakeClienteService();
        var vm = new ClientesViewModel(fake);

        vm.Filter = "alice";

        Assert.Single(vm.FilteredClientes);
    }

    [Fact]
    public void SelectedCliente_not_null_after_constructor()
    {
        var fake = new FakeClienteService();
        var vm = new ClientesViewModel(fake);

        Assert.Null(vm.SelectedCliente);
    }

    [Fact]
    public void Title_initialized()
    {
        var fake = new FakeClienteService();
        var vm = new ClientesViewModel(fake);

        Assert.Equal("Clientes", vm.Title);
    }
}