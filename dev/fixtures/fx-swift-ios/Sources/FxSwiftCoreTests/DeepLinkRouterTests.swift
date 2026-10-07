import Testing
import Foundation
@testable import FxSwiftCore

@Suite("DeepLinkRouter")
struct DeepLinkRouterTests {
    @Test("onboarding route is parsed")
    func onboardingRoute() {
        let url = URL(string: "fxswift://onboarding")!
        let route = DeepLinkRouter.handle(url)
        #expect(route?.destination == .onboarding)
    }

    @Test("expense route with id is parsed")
    func expenseRouteWithId() {
        let id = UUID()
        let url = URL(string: "fxswift://expense?id=\(id.uuidString)")!
        let route = DeepLinkRouter.handle(url)
        #expect(route?.destination == .expenseDetail(id: id))
    }

    @Test("unknown scheme returns nil")
    func unknownSchemeReturnsNil() {
        let url = URL(string: "https://example.com/foo")!
        let route = DeepLinkRouter.handle(url)
        #expect(route == nil)
    }
}
