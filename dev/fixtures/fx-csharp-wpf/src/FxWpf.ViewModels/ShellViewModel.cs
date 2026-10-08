using CommunityToolkit.Mvvm.ComponentModel;

namespace FxWpf.ViewModels;

public partial class ShellViewModel : ObservableObject
{
    [ObservableProperty]
    private string _title = "FxWpf";

    [ObservableProperty]
    private string _currentView = "Clientes";
}