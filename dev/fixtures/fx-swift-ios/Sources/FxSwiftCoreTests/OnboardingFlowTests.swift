import Testing
import Foundation
@testable import FxSwiftCore

@Suite("OnboardingFlow")
struct OnboardingFlowTests {
    @Test("intro transitions to permissions")
    func introGoesToPermissions() {
        let next = OnboardingState.intro.next()
        #expect(next == .permissions(askNotifications: true))
    }

    @Test("permissions transitions to iCloud")
    func permissionsGoesToICloud() {
        let next = OnboardingState.permissions(askNotifications: false).next()
        #expect(next == .iCloud(available: true))
    }

    @Test("done has no next state")
    func doneHasNoNext() {
        let next = OnboardingState.done(completedAt: Date()).next()
        #expect(next == nil)
    }
}
