using System;
using System.Globalization;
using System.Windows.Data;

namespace FxWpf.App.Converters;

public class CurrencyConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is decimal d)
        {
            return d.ToString("C", culture);
        }
        if (value is double dbl)
        {
            return dbl.ToString("C", culture);
        }
        return "$0.00";
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is string str)
        {
            var trimmed = str.Replace("$", "").Replace(",", "").Trim();
            return decimal.TryParse(trimmed, NumberStyles.Currency, culture, out var d) ? d : 0m;
        }
        return 0m;
    }
}