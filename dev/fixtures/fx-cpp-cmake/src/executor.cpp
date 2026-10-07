#include "fxproc/executor.hpp"

#include <atomic>
#include <future>
#include <thread>
#include <vector>

namespace fxproc {

namespace {
std::atomic<size_t> g_active{0};
}  // namespace

// P01 trampa: thread_no_join. El thread se detach()a en lugar de
// join()arse, asi que el thread queda zombie hasta std::terminate.
// En esta fixture lo hacemos de forma que el test pueda observar
// el conteo de threads activos sin causar UB en el teardown.
std::future<std::string> Executor::submit(Task task) {
    auto promise = std::make_shared<std::promise<std::string>>();
    auto future = promise->get_future();
    g_active.fetch_add(1);
    std::thread([task = std::move(task), promise, lifetime = std::shared_ptr<void>(nullptr)]() mutable {
        try {
            promise->set_value(task());
        } catch (...) {
            try { promise->set_exception(std::current_exception()); } catch (...) {}
        }
        g_active.fetch_sub(1);
    }).detach();  // P01: detach en lugar de join.
    return future;
}

std::string Executor::run_with_timeout(Task task, std::chrono::milliseconds timeout) {
    auto fut = submit(std::move(task));
    if (fut.wait_for(timeout) == std::future_status::timeout) {
        throw TimeoutError("task exceeded timeout");
    }
    return fut.get();
}

size_t Executor::active_threads() {
    return g_active.load();
}

}  // namespace fxproc
