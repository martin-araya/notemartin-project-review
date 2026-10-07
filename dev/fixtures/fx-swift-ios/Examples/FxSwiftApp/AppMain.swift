import SwiftUI
import FxSwiftCore

@main
struct FxSwiftApp: App {
    var body: some Scene {
        WindowGroup {
            OnboardingView()
                .onOpenURL { url in
                    _ = DeepLinkRouter.handle(url)
                }
        }
    }
}
