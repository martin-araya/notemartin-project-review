// S02: unused_helper. Tres funciones obsoletas sin marca
// de deprecation. La trampa es que el codigo de la app puede
// seguirlas usando sin warning del compilador. La skill debe
// detectar la falta de la marca de deprecation para catalogar la
// trampa superficial #2.
#pragma once

#include <string>
#include <vector>

namespace fxproc::util {

// Las siguientes funciones quedaron obsoletas en 0.0.5 pero no se marco
// la marca de deprecation; todavia se usan en scripts de migracion
// internos. La trampa superficial es esa falta de marca.

inline std::string old_slugify(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (std::isalnum(static_cast<unsigned char>(c))) {
            out += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        } else if (c == ' ' || c == '-') {
            out += '_';
        }
    }
    return out;
}

inline std::vector<std::string> split_comma_old(const std::string& s) {
    std::vector<std::string> out;
    std::string current;
    for (char c : s) {
        if (c == ',') {
            if (!current.empty()) out.push_back(current);
            current.clear();
        } else {
            current += c;
        }
    }
    if (!current.empty()) out.push_back(current);
    return out;
}

inline int legacy_counter() {
    static int n = 0;
    return ++n;
}

}  // namespace fxproc::util
