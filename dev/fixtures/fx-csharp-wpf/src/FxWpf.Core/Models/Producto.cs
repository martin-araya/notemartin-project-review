namespace FxWpf.Core.Models;

public class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
    public string Sku { get; set; } = string.Empty;
}