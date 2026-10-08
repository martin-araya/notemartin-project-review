// UrlSessionProviderTests.swift
// Tests que verifican la trampa E6 (#if canImport(FoundationNetworking)).
import XCTest
@testable import FxSwiftServer

final class UrlSessionProviderTests: XCTestCase {
    func testMakeSessionReturnsNonNil() {
        let s1 = UrlSessionProvider.makeSession()
        XCTAssertNotNil(s1)
    }

    func testMakeSessionCustomTimeout() {
        let s2 = UrlSessionProvider.makeSession(timeout: 60.0)
        XCTAssertNotNil(s2)
    }

    func testMakeSessionDefaultInLinux() {
        // En Linux FoundationNetworking siempre esta disponible, asi que
        // la rama del `if` siempre devuelve una session con `.default`.
        #if canImport(FoundationNetworking)
        let session = UrlSessionProvider.makeSession()
        XCTAssertNotNil(session.configuration)
        #else
        let session = UrlSessionProvider.makeSession()
        XCTAssertNotNil(session)
        #endif
    }
}