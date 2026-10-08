package com.example.fxandroid.domain.model

data class HistoryEntry(
    val id: Long,
    val actor: String,
    val action: String,
    val targetId: String,
    val createdAt: Long
)