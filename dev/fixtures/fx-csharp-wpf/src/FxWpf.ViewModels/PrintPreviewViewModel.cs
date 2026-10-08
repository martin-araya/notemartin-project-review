using CommunityToolkit.Mvvm.ComponentModel;

namespace FxWpf.ViewModels;

public partial class PrintPreviewViewModel : ObservableObject
{
    [ObservableProperty]
    private string _documentPath = string.Empty;

    [ObservableProperty]
    private string _status = "Listo";

    [ObservableProperty]
    private bool _isValid = true;
}