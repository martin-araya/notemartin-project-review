package com.example.fxandroid.ui.legacy

import android.view.LayoutInflater
import android.view.ViewGroup
import com.example.fxandroid.databinding.ActivityLegacyProductBinding

object LegacyBindingAdapter {
    fun inflate(inflater: LayoutInflater, parent: ViewGroup?): ActivityLegacyProductBinding {
        return ActivityLegacyProductBinding.inflate(inflater, parent, false)
    }
}