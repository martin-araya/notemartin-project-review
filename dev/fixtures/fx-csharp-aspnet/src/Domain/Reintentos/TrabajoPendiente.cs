namespace FxAspNet.Domain.Reintentos;

public class TrabajoPendiente
{
    public int Id { get; set; }
    public string Tipo { get; set; } = string.Empty;
    public string Payload { get; set; } = string.Empty;
    public int Intentos { get; set; }
    public DateTimeOffset? UltimoIntentoEn { get; set; }
    public TrabajoEstado Estado { get; set; }
    public DateTimeOffset CreadoEn { get; set; }
}