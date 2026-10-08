// ErrorDTO.swift
import Foundation
import Vapor

struct ErrorDTO: Codable, Content, Sendable {
    var error: String
    var detail: String?
    init(error: String, detail: String? = nil) {
        self.error = error
        self.detail = detail
    }
}