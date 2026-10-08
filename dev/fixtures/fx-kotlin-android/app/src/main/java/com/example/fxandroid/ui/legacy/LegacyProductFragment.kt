package com.example.fxandroid.ui.legacy

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

/**
 * Trampa S3: este Fragment esta declarado pero su onCreateView devuelve null.
 * No hace nada util. Existe solo para mostrar codigo muerto.
 */
class LegacyProductFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return null
    }
}