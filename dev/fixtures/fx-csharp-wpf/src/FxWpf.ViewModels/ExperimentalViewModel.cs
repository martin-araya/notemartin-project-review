using CommunityToolkit.Mvvm.ComponentModel;

namespace FxWpf.ViewModels;

/// <summary>
/// Trampa S3: ViewModel declarado pero no se usa en runtime.
/// La skill debe detectar que no esta referenciado en ninguna View.
/// </summary>
public partial class ExperimentalViewModel : ObservableObject
{
    [ObservableProperty]
    private string _experimentName = string.Empty;

    [ObservableProperty]
    private bool _isExperimental = false;
}