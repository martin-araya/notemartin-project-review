#include <filesystem>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "fxproc/version.hpp"
#include "fxproc/registry.hpp"
#include "fxproc/pipeline.hpp"
#include "fxproc/plugin_loader.hpp"
#include "fxproc/executor.hpp"
#include "fxproc/filter_base.hpp"

namespace fs = std::filesystem;

namespace {

void print_usage() {
    std::cout <<
        "fxproc - motor de procesamiento con plugins\n"
        "Uso:\n"
        "  fxproc list                              Lista los filtros registrados.\n"
        "  fxproc run <pipeline> <input>            Corre un pipeline sobre input.\n"
        "  fxproc load <plugin.so>                   Carga un plugin via dlopen.\n"
        "  fxproc version                            Imprime la version.\n"
        "\n"
        "Pipelines disponibles: to_upper, reverse, json, all\n";
}

bool parse_flag(const std::vector<std::string>& args, const std::string& flag, std::string& out) {
    for (size_t i = 1; i + 1 < args.size(); ++i) {
        if (args[i] == flag) {
            out = args[i + 1];
            return true;
        }
    }
    return false;
}

std::string run_pipeline(const std::string& name, const std::string& input) {
    auto& reg = fxproc::Registry::instance();
    if (!reg.has(name)) {
        throw std::runtime_error("filter not found: " + name);
    }
    auto f = reg.create(name);
    return f->run(input);
}

}  // namespace

int main(int argc, char** argv) {
    std::vector<std::string> args(argv, argv + argc);
    if (args.size() < 2) {
        print_usage();
        return 1;
    }

    const std::string cmd = args[1];

    try {
        if (cmd == "version") {
            std::cout << fxproc::version() << std::endl;
            return 0;
        }
        if (cmd == "list") {
            for (const auto& n : fxproc::Registry::instance().names()) {
                std::cout << n << std::endl;
            }
            return 0;
        }
        if (cmd == "load") {
            if (args.size() < 3) {
                std::cerr << "load requiere <plugin.so>" << std::endl;
                return 2;
            }
            fxproc::PluginLoader loader;
            size_t n = loader.load(args[2]);
            std::cout << "OK loaded " << n << " filters from " << args[2] << std::endl;
            return 0;
        }
        if (cmd == "run") {
            if (args.size() < 4) {
                std::cerr << "run requiere <pipeline> <input>" << std::endl;
                return 2;
            }
            std::cout << run_pipeline(args[2], args[3]) << std::endl;
            return 0;
        }
        if (cmd == "version-flags") {
            std::cout << "FX_VERSION=" << fxproc::version()
                      << " FX_HAS_PLUGINS=" << fxproc::has_plugins() << std::endl;
            return 0;
        }
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << std::endl;
        return 3;
    }

    print_usage();
    return 1;
}
