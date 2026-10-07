#pragma once

#include <stdexcept>
#include <string>

namespace fxproc {

class ExportError : public std::runtime_error {
public:
    explicit ExportError(const std::string& msg) : std::runtime_error(msg) {}
};

class Exporter {
public:
    // Escribe `content` a stdout con un newline final.
    static void to_stdout(const std::string& content);

    // Escribe `content` al archivo en `path`. Lanza ExportError si
    // el path no es escribible o si la escritura falla.
    static void to_file(const std::string& path, const std::string& content);

    // Serializadores a string.
    static std::string to_json_string(const std::string& key, const std::string& value);
    static std::string to_csv_string(const std::string& key, const std::string& value);
};

}  // namespace fxproc
