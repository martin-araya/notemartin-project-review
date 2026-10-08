package com.example.fxandroid

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class FxAndroidApp : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}