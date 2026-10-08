package com.example.fxandroid.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.example.fxandroid.work.SyncScheduler

class SyncTriggerReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        SyncScheduler().scheduleOnce()
    }
}