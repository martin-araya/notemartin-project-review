/* F06y: Unity internals - implementacion de las funciones declaradas
 * en unity.h. Este archivo se compila con cada test para resolver
 * los simbolos de Unity.
 *
 * Si se compila con HOST_TEST=1, los tests linkean contra el stub
 * `_exit` y `printf` que viven en hal_host.c. Si se compila para bare-metal,
 * hay que definir estos simbolos en startup.c.
 */
#include "unity.h"

#include <stdio.h>
#include <string.h>

const char* UnityCurrentTestName = "(no test)";

static int UnityTestFailed = 0;
static int UnityTestIgnored = 0;
int UnityCurrentTestFailed = 0;
static int UnityCurrentTestIgnored = 0;
static int UnityNumberOfTests = 0;
static int UnityTestNumber = 0;
static int UnityVerbose = 1;
static const char* UnityCurrentSuiteName = NULL;

void UnityBegin(const char* file)
{
    UnityTestFailed = 0;
    UnityTestIgnored = 0;
    UnityNumberOfTests = 0;
    UnityCurrentSuiteName = file;
    if (UnityVerbose) {
        printf("Unity test run starting for %s\n", file);
    }
}

int UnityEnd(void)
{
    if (UnityVerbose) {
        printf("\nUnity tests: %d failed (%d), %d ignored (%d), %d total\n",
               UnityTestFailed, UnityTestNumber,
               UnityTestIgnored, UnityNumberOfTests,
               UnityNumberOfTests);
    }
    return UnityTestFailed;
}

void UnityReport(int line)
{
    UnityNumberOfTests++;
    UnityTestNumber++;
    if (UnityCurrentTestIgnored) {
        UnityTestIgnored++;
        UnityCurrentTestIgnored = 0;
        if (UnityVerbose) {
            printf("IGNORE: %s:%d\n", UnityCurrentTestName, line);
        }
    } else if (UnityCurrentTestFailed) {
        UnityTestFailed++;
        UnityCurrentTestFailed = 0;
        if (UnityVerbose) {
            printf("FAIL: %s:%d\n", UnityCurrentTestName, line);
        }
    } else {
        if (UnityVerbose) {
            printf("PASS: %s:%d\n", UnityCurrentTestName, line);
        }
    }
}

void UnityAssertEqualNumber(int expected, int actual,
                            const char* msg, int line)
{
    if (expected != actual) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (expected %d, got %d)\n",
               line, msg, expected, actual);
    }
}

void UnityAssertEqualString(const char* expected, const char* actual,
                             const char* msg, int line)
{
    if (expected == NULL || actual == NULL) {
        if (expected != actual) {
            UnityCurrentTestFailed = 1;
            printf("  ASSERT FAILED at line %d: %s (one is NULL)\n", line, msg);
        }
        return;
    }
    if (strcmp(expected, actual) != 0) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (expected \"%s\", got \"%s\")\n",
               line, msg, expected, actual);
    }
}

void UnityAssertNull(const void* ptr, const char* msg, int line)
{
    if (ptr != NULL) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (pointer not NULL)\n", line, msg);
    }
}

void UnityAssertNotNull(const void* ptr, const char* msg, int line)
{
    if (ptr == NULL) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (pointer is NULL)\n", line, msg);
    }
}

void UnityAssertTrue(int condition, const char* msg, int line)
{
    if (!condition) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s\n", line, msg);
    }
}

void UnityAssertFalse(int condition, const char* msg, int line)
{
    if (condition) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (expected false)\n", line, msg);
    }
}

void UnityAssertGreaterOrEqualNumber(int threshold, int actual,
                                     const char* msg, int line)
{
    if (actual < threshold) {
        UnityCurrentTestFailed = 1;
        printf("  ASSERT FAILED at line %d: %s (got %d, expected >= %d)\n",
               line, msg, actual, threshold);
    }
}

/* setUp/tearDown como weak symbols; los tests que no las necesitan
 * no las definen. */
__attribute__((weak)) void setUp(void) {}
__attribute__((weak)) void tearDown(void) {}
