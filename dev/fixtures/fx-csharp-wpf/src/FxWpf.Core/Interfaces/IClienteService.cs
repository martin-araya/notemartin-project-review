using System.Collections.Generic;
using System.Threading.Tasks;
using FxWpf.Core.Models;

namespace FxWpf.Core.Interfaces;

public interface IClienteService
{
    Task<List<Cliente>> GetAllAsync();
    Task<Cliente?> GetByIdAsync(int id);
    Task<Cliente> CreateAsync(Cliente cliente);
    Task<Cliente?> UpdateAsync(Cliente cliente);
    Task<bool> DeleteAsync(int id);
}