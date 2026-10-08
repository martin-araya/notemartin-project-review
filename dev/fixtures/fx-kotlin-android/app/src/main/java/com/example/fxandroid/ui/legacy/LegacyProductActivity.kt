package com.example.fxandroid.ui.legacy

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.os.Bundle
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fxandroid.databinding.ActivityLegacyProductBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class LegacyProductActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLegacyProductBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLegacyProductBinding.inflate(layoutInflater)
        setContentView(binding.root)
    }

    /**
     * Trampa P5: este método es el handler del `android:onClick="onSaveClick"`
     * declarado en activity_legacy_product.xml. La skill debe notar que
     * NO usa el repository ni Hilt: escribe directamente en SQLite con
     * `execSQL`, bypassing todas las capas de abstraccion.
     */
    fun onSaveClick(view: View) {
        val ean = binding.legacyEan.text.toString()
        val db: SQLiteDatabase = openOrCreateDatabase("fx_legacy.db", Context.MODE_PRIVATE, null)
        db.execSQL("INSERT INTO legacy_products(ean) VALUES('$ean')")
        db.close()
        Toast.makeText(this, "Guardado legacy", Toast.LENGTH_SHORT).show()
    }
}