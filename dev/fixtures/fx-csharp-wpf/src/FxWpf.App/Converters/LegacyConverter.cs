using System;
using System.Globalization;
using System.Windows.Data;

namespace FxWpf.App.Converters;

/// <summary>
/// Trampa S1: converter declarado pero no invocado en ningun XAML.
/// La skill debe verificar que no aparece en Resources ni en StaticResource.
/// </summary>
public class LegacyConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        return value;
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        return value!;
    }
}