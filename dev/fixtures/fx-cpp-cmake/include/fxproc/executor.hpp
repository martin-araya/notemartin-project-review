// Executor: corre el pipeline en threads separados. La trampa
// paquete P01 (thread_no_join) planta un bug en este executor:
// los threads se detach()an en lugar de join()arse, lo que
// produce threads zombies hasta std::terminate al final del proceso.
#pragma once

#include <chrono>
#include <functional>
#include <future>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace fxproc {

class TimeoutError : public std::runtime_error {
public:
    explicit TimeoutError(const std::string& msg) : std::runtime_error(msg) {}
};

// Ejecuta `task` en un thread. La trampa P01 lo planta con detach()
// en lugar de join() para que los threads queden zombies.
class Executor {
public:
    using Task = std::function<std::string()>;

    // P01: thread_with_no_join. El thread se detach y nunca se join.
    // Documentado y verificado por test que mide el conteo de threads.
    std::future<std::string> submit(Task task);

    // Ejecuta con timeout. Lanza TimeoutError si task no termina.
    std::string run_with_timeout(Task task,
                                 std::chrono::milliseconds timeout);

    // Tamano aproximado del pool (util para tests que verifican P01).
    static size_t active_threads();
};

}  // namespace fxproc
