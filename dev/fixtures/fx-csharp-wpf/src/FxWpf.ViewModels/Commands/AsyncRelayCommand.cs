using System;
using System.Threading.Tasks;
using System.Windows.Input;

namespace FxWpf.ViewModels.Commands;

/// <summary>
/// Trampa P5: ICommand custom con CanExecute que retorna false siempre.
/// El comando nunca se habilita, incluso cuando el usuario interactua.
/// </summary>
public class AsyncRelayCommand : ICommand
{
    private readonly Func<Task> _execute;
    private readonly Func<bool>? _canExecute;

    public AsyncRelayCommand(Func<Task> execute, Func<bool>? canExecute = null)
    {
        _execute = execute ?? throw new ArgumentNullException(nameof(execute));
        _canExecute = canExecute;
    }

    public bool CanExecute(object? parameter)
    {
        // Trampa P5: canExecute siempre retorna false.
        // En runtime, el boton UI nunca se habilita.
        return false;
    }

    public async void Execute(object? parameter)
    {
        await _execute();
    }

    public event EventHandler? CanExecuteChanged
    {
        add { }
        remove { }
    }
}