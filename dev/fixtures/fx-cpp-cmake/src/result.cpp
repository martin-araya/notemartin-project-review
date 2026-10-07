#include "fxproc/result.hpp"

#include <cerrno>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>

namespace fxproc {

namespace fs = std::filesystem;

void Exporter::to_stdout(const std::string& content) {
    std::cout << content << std::endl;
}

void Exporter::to_file(const std::string& path, const std::string& content) {
    fs::path p(path);
    // P04 trampa: export_race. Abrimos sin flag exclusivo y sin lock;
    // otro thread puede leer el archivo mientras escribimos.
    std::ofstream out(p, std::ios::binary | std::ios::trunc);
    if (!out) {
        // Reportamos el errno via what() para que el test verifique el
        // mensaje exacto.
        throw ExportError("open failed: " + p.string() + ": " +
                          std::strerror(errno));
    }
    out << content;
    if (!out) {
        throw ExportError("write failed: " + p.string() + ": " +
                          std::strerror(errno));
    }
}

std::string Exporter::to_json_string(const std::string& key, const std::string& value) {
    std::ostringstream os;
    os << "{\"" << key << "\":\"" << value << "\"}";
    return os.str();
}

std::string Exporter::to_csv_string(const std::string& key, const std::string& value) {
    std::ostringstream os;
    os << key << "," << value << std::endl;
    return os.str();
}

}  // namespace fxproc
