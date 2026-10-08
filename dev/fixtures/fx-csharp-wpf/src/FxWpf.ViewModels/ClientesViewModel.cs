using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using FxWpf.Core.Interfaces;
using FxWpf.Core.Models;

namespace FxWpf.ViewModels;

/// <summary>
/// Trampa E2: ViewModel con [ObservableProperty] y [RelayCommand] de CommunityToolkit.Mvvm.
/// El codigo generado (propiedades publicas + commands) vive en obj/Debug/.../generated/.
/// Trampa P1: OnSelectedClienteChanged sin null check (DisplayCliente lanza NRE).
/// </summary>
public partial class ClientesViewModel : ObservableObject
{
    private readonly IClienteService _clienteService;

    public ClientesViewModel(IClienteService clienteService)
    {
        _clienteService = clienteService;
        Clientes = new ObservableCollection<Cliente>();
        Clientes.Add(new Cliente { Id = 1, Nombre = "Alice", Email = "alice@fxwpf.com" });
        Clientes.Add(new Cliente { Id = 2, Nombre = "Bob", Email = "bob@fxwpf.com" });
    }

    [ObservableProperty]
    private string _title = "Clientes";

    [ObservableProperty]
    private ObservableCollection<Cliente> _clientes = new();

    [ObservableProperty]
    private Cliente? _selectedCliente;

    [ObservableProperty]
    private string _filter = string.Empty;

    [ObservableProperty]
    private string _statusMessage = "Listo";

    public IEnumerable<Cliente> FilteredClientes =>
        string.IsNullOrWhiteSpace(Filter)
            ? Clientes
            : Clientes.Where(c => c.Nombre.Contains(Filter, StringComparison.OrdinalIgnoreCase));

    /// <summary>
    /// Trampa P1: el partial method se invoca al cambiar SelectedCliente.
    /// Aqui NO validamos null; si el usuario clickea un cliente eliminado,
    /// DisplayCliente(null) lanza NullReferenceException.
    /// </summary>
    partial void OnSelectedClienteChanged(Cliente? oldValue, Cliente? newValue)
    {
        DisplayCliente(newValue); // Trampa P1: sin null check
    }

    private void DisplayCliente(Cliente? cliente)
    {
        if (cliente is null)
        {
            StatusMessage = "Seleccion nula";
            return;
        }
        StatusMessage = $"Mostrando {cliente.Email}";
    }

    [RelayCommand]
    private async Task AddCliente()
    {
        var cliente = new Cliente
        {
            Id = Clientes.Count + 1,
            Nombre = $"Cliente {Clientes.Count + 1}",
            Email = $"nuevo{Clientes.Count + 1}@fxwpf.com",
        };
        await _clienteService.CreateAsync(cliente);
        Clientes.Add(cliente);
        StatusMessage = $"Agregado {cliente.Nombre}";
    }

    [RelayCommand]
    private void FilterClientes(string query)
    {
        Filter = query;
        OnPropertyChanged(nameof(FilteredClientes));
    }
}