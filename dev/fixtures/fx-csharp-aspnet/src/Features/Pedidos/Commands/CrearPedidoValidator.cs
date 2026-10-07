namespace FxAspNet.Features.Pedidos.Commands;

public static class CrearPedidoValidator
{
    public static List<string> Validar(CrearPedidoCommand cmd)
    {
        var errores = new List<string>();
        if (string.IsNullOrWhiteSpace(cmd.Cliente))
            errores.Add("cliente_requerido");
        if (cmd.Items is null || cmd.Items.Count == 0)
            errores.Add("items_requeridos");
        foreach (var item in cmd.Items ?? new List<PedidoItemDto>())
        {
            if (item.Cantidad <= 0)
                errores.Add($"cantidad_invalida:{item.Sku}");
        }
        return errores;
    }
}