using System.Collections.Generic;
using System.Threading.Tasks;
using FxWpf.Core.Interfaces;
using FxWpf.Core.Models;

namespace FxWpf.Tests;

internal sealed class FakeClienteService : IClienteService
{
    public List<Cliente> Items { get; } = new();

    public Task<List<Cliente>> GetAllAsync() => Task.FromResult(Items);

    public Task<Cliente?> GetByIdAsync(int id) =>
        Task.FromResult(Items.Find(c => c.Id == id));

    public Task<Cliente> CreateAsync(Cliente cliente)
    {
        cliente.Id = Items.Count + 1;
        Items.Add(cliente);
        return Task.FromResult(cliente);
    }

    public Task<Cliente?> UpdateAsync(Cliente cliente)
    {
        var existing = Items.Find(c => c.Id == cliente.Id);
        if (existing is null) return Task.FromResult<Cliente?>(null);
        existing.Nombre = cliente.Nombre;
        existing.Email = cliente.Email;
        existing.Telefono = cliente.Telefono;
        return Task.FromResult<Cliente?>(existing);
    }

    public Task<bool> DeleteAsync(int id)
    {
        var idx = Items.FindIndex(c => c.Id == id);
        if (idx == -1) return Task.FromResult(false);
        Items.RemoveAt(idx);
        return Task.FromResult(true);
    }
}