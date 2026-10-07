namespace FxAspNet.Domain.Facturacion;

public class Factura
{
    public int Id { get; set; }
    public int PedidoId { get; set; }
    public string Numero { get; set; } = string.Empty;
    public DateTimeOffset EmitidaEn { get; set; }
    public decimal Importe { get; set; }
    public FacturaEstado Estado { get; set; }
}