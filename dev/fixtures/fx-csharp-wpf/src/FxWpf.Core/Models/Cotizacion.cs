using System;
using System.Collections.Generic;

namespace FxWpf.Core.Models;

public class Cotizacion
{
    public int Id { get; set; }
    public string Titulo { get; set; } = string.Empty;
    public int ClienteId { get; set; }
    public DateTime Fecha { get; set; } = DateTime.UtcNow;
    public decimal Subtotal { get; set; }
    public decimal Iva { get; set; }
    public decimal Total { get; set; }
    public string Moneda { get; set; } = "USD";
    public List<CotizacionItem> Items { get; set; } = new();
}

public class CotizacionItem
{
    public int Id { get; set; }
    public int CotizacionId { get; set; }
    public int ProductoId { get; set; }
    public int Cantidad { get; set; }
    public decimal PrecioUnitario { get; set; }
    public decimal Subtotal { get; set; }
}