package com.fxmin;

/**
 * Interfaz base para las features. Las implementaciones se registran en
 * META-INF/services/com.fxmin.Feature (ServiceLoader).
 */
public interface Feature {
    String name();
}