using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using FxWpf.Core.Models;

namespace FxWpf.ViewModels;

/// <summary>
/// Trampa P2: SaveCotizacion usa Task.Run sin await.
/// En runtime la operacion bloquea el thread de UI.
/// </summary>
public partial class CotizacionesViewModel : ObservableObject
{
    [ObservableProperty]
    private string _title = "Cotizaciones";

    [ObservableProperty]
    private ObservableCollection<Cotizacion> _cotizaciones = new();

    [ObservableProperty]
    private Cotizacion? _selectedCotizacion;

    [ObservableProperty]
    private string _moneda = "USD";

    [ObservableProperty]
    private string _filter = string.Empty;

    public CotizacionesViewModel()
    {
        Cotizaciones.Add(new Cotizacion
        {
            Id = 1,
            Titulo = "Cotizacion inicial",
            ClienteId = 1,
            Subtotal = 1000m,
            Iva = 130m,
            Total = 1130m,
            Moneda = "USD",
        });
    }

    [RelayCommand]
    private void SaveCotizacion()
    {
        // Trampa P2: Task.Run sin await bloquea el UI thread.
        if (SelectedCotizacion is null) return;
        Task.Run(() =>
        {
            // Simulacion de I/O bloqueante
            System.Threading.Thread.Sleep(2000);
        });
    }

    [RelayCommand(CanExecute = nameof(CanAddCotizacion))]
    private void AddCotizacion()
    {
        Cotizaciones.Add(new Cotizacion
        {
            Id = Cotizaciones.Count + 1,
            Titulo = $"Nueva #{Cotizaciones.Count + 1}",
            ClienteId = 1,
            Moneda = Moneda,
        });
    }

    private bool CanAddCotizacion() => !string.IsNullOrWhiteSpace(Moneda);
}