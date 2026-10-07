//! Trampa E03: codigo gated por `#[cfg(feature = "legacy")]`.
//!
//! Solo se compila con `--features legacy`. Por defecto no se incluye
//! en el binario. La skill debe notar el `#[cfg(feature = "...")]`
//! para entender que codigo esta activo. Es codigo dead en runtime
//! (trampa superficial S02).

#[cfg(feature = "legacy")]
pub struct LegacyEvent {
    pub id: i64,
    pub data: String,
}

#[cfg(feature = "legacy")]
impl LegacyEvent {
    pub fn hash(&self) -> u64 {
        // Hash trivial solo para uso en codigo legacy.
        self.data.bytes().fold(0u64, |acc, b| acc.wrapping_mul(31).wrapping_add(b as u64))
    }
}
