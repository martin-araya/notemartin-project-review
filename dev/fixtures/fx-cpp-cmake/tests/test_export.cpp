// F06x: tests de exportacion (Exporter).
#include "fxproc/result.hpp"

#include <cstdio>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <string>

namespace fs = std::filesystem;

TEST(Exporter, ToStdoutDoesNotThrow) {
    EXPECT_NO_THROW(fxproc::Exporter::to_stdout("hello"));
}

TEST(Exporter, ToFileWritesContent) {
    fs::path tmp = fs::temp_directory_path() / "fxproc_test_out.txt";
    fxproc::Exporter::to_file(tmp.string(), "hello world");
    ASSERT_TRUE(fs::exists(tmp));
    std::ifstream in(tmp);
    std::string content((std::istreambuf_iterator<char>(in)),
                         std::istreambuf_iterator<char>());
    EXPECT_EQ(content, "hello world");
    fs::remove(tmp);
}

TEST(Exporter, ToJsonStringContainsKeyAndValue) {
    std::string s = fxproc::Exporter::to_json_string("name", "fxproc");
    EXPECT_NE(s.find("name"), std::string::npos);
    EXPECT_NE(s.find("fxproc"), std::string::npos);
}
