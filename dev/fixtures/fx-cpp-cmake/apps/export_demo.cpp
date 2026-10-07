// apps/export_demo.cpp - binario de ejemplo que usa Exporter para
// persistir un resultado. Usado en el R-01 de exportar-resultados.
#include "fxproc/result.hpp"

#include <cstdlib>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "uso: export_demo <key> <value> [output_path]" << std::endl;
        return 1;
    }
    std::string key = argv[1];
    std::string value = argv[2];
    std::string content = fxproc::Exporter::to_json_string(key, value);
    if (argc >= 4) {
        try {
            fxproc::Exporter::to_file(argv[3], content);
            std::cout << "OK wrote " << content.size() << " bytes to " << argv[3] << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "ERROR: " << e.what() << std::endl;
            return 2;
        }
    } else {
        fxproc::Exporter::to_stdout(content);
    }
    return 0;
}
