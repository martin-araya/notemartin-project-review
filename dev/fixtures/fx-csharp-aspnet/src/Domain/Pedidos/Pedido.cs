namespace FxAspNet.Domain.Pedidos;

public class Pedido
{
    public int Id { get; set; }
    public string Cliente { get; set; } = string.Empty;
    public DateTimeOffset CreadoEn { get; set; }
    public decimal Total { get; set; }
    public PedidoEstado Estado { get; set; }
    public List<PedidoItem> Items { get; set; } = new();
}