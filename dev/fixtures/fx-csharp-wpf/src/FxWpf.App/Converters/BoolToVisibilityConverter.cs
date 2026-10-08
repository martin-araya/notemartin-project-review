using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace FxWpf.App.Converters;

/// <summary>
/// Trampa E4 + P3: IValueConverter con ConvertBack que lanza NotImplementedException.
/// Trampa E6 + P3 combinado: si la UI intenta bindear en modo TwoWay,
/// falla en runtime con NotImplementedException.
/// </summary>
public class BoolToVisibilityConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is bool b)
        {
            return b ? Visibility.Visible : Visibility.Collapsed;
        }
        return Visibility.Collapsed;
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        // Trampa P3: ConvertBack no implementado.
        throw new NotImplementedException("BoolToVisibilityConverter.ConvertBack no implementado");
    }
}