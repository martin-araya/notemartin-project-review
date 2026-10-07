/* F06y: Unity test framework - ThrowTheSwitch (MIT License, version 2.5.2)
 *
 * Single-header embedido en include/tests/unity.h. La version original
 * esta en https://www.thruswitch.com/unity/. Esta copia es una version
 * minima que cubre RUN_TEST/TEST_ASSERT y los tipos basicos necesarios
 * para los tests del fixture.
 *
 * Si necesitas features adicionales (mocks, fixtures con setUp/tearDown
 * avanzado, parametros), descarga el tarball oficial y reemplaza este
 * header + el unity_internals.h correspondiente.
 */
#ifndef FXEMB_UNITY_H
#define FXEMB_UNITY_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

void UnityBegin(const char* file);
int  UnityEnd(void);
void UnityAssertEqualNumber(int expected, int actual,
                            const char* msg, int line);
void UnityAssertEqualString(const char* expected, const char* actual,
                             const char* msg, int line);
void UnityAssertNull(const void* ptr, const char* msg, int line);
void UnityAssertNotNull(const void* ptr, const char* msg, int line);
void UnityAssertTrue(int condition, const char* msg, int line);
void UnityAssertFalse(int condition, const char* msg, int line);
void UnityAssertGreaterOrEqualNumber(int threshold, int actual,
                                     const char* msg, int line);

/* Macros de asercion. */
#define TEST_ASSERT_EQUAL_INT(expected, actual) \
    UnityAssertEqualNumber((int)(expected), (int)(actual), \
                           #expected " == " #actual, __LINE__)
#define TEST_ASSERT_EQUAL_STRING(expected, actual) \
    UnityAssertEqualString((expected), (actual), \
                            #expected " == " #actual, __LINE__)
#define TEST_ASSERT_NULL(ptr) \
    UnityAssertNull((ptr), #ptr " is NULL", __LINE__)
#define TEST_ASSERT_NOT_NULL(ptr) \
    UnityAssertNotNull((ptr), #ptr " is not NULL", __LINE__)
#define TEST_ASSERT_TRUE(condition) \
    UnityAssertTrue((int)(condition), #condition " is true", __LINE__)
#define TEST_ASSERT_FALSE(condition) \
    UnityAssertFalse((int)(condition), #condition " is false", __LINE__)
#define TEST_ASSERT_GREATER_OR_EQUAL_INT(threshold, actual) \
    UnityAssertGreaterOrEqualNumber((int)(threshold), (int)(actual), \
                                    #actual " >= " #threshold, __LINE__)
#define TEST_FAIL_MESSAGE(msg) \
    do { \
        UnityCurrentTestFailed = 1; \
        printf("  FAIL at line %d: %s\n", __LINE__, msg); \
    } while (0)

/* Macros de declaracion de test. */
#define RUN_TEST(func) UnityCurrentTestName = #func; \
    setUp(); func(); tearDown(); UnityReport(__LINE__)

/* setUp/tearDown opcionales. Las funciones se declaran weak para que
 * los tests no necesiten redefinirlas. */
extern const char* UnityCurrentTestName;
extern int UnityCurrentTestFailed;
void UnityReport(int line);

void setUp(void);
void tearDown(void);

#ifdef __cplusplus
}
#endif

#endif /* FXEMB_UNITY_H */
