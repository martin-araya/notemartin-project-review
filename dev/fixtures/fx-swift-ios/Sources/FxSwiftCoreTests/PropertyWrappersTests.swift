import Testing
import Foundation
@testable import FxSwiftCore

@Suite("PropertyWrappers")
struct PropertyWrappersTests {
    @Test("Debounced stores initial value")
    func debouncedStoresInitialValue() {
        let debounced = Debounced(wrappedValue: "initial", delay: 0.5)
        #expect(debounced.wrappedValue == "initial")
    }

    @Test("Debounced set immediately writes synchronously")
    func debouncedSetImmediatelyWritesSynchronously() {
        let debounced = Debounced(wrappedValue: 0, delay: 0.5)
        debounced.set(42, immediately: true)
        #expect(debounced.wrappedValue == 42)
    }

    @Test("Debounced set delayed applies after delay")
    func debouncedSetDelayedAppliesAfterDelay() async {
        let debounced = Debounced(wrappedValue: 0, delay: 0.05)
        debounced.set(7)
        try? await Task.sleep(nanoseconds: 200_000_000)
        #expect(debounced.wrappedValue == 7)
    }

    @Test("UserDefaultsBacked round-trips a value")
    func userDefaultsBackedRoundTrip() {
        let key = "fxswift-test-\(UUID().uuidString)"
        let suite = UserDefaults(suiteName: "fxswift-tests-\(UUID().uuidString)")!
        let wrapped = UserDefaultsBacked(wrappedValue: "default", key, store: suite)
        #expect(wrapped.wrappedValue == "default")
        wrapped.wrappedValue = "actualizado"
        #expect(wrapped.wrappedValue == "actualizado")
    }
}
