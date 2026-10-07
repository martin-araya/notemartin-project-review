namespace FxAspNet.Domain.Pedidos;

public partial class PedidoItem
{
    public int Id { get; set; }
    public int PedidoId { get; set; }
    public string Sku { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public decimal PrecioUnitario { get; set; }
}