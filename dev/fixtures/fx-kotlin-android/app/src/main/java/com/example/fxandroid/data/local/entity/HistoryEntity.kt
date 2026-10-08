package com.example.fxandroid.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "history")
data class HistoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val actor: String,
    val action: String,
    val targetId: String,
    val createdAt: Long
)