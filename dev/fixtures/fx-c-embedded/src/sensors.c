/* F06y: sensors.c - feature 1: lectura de sensores. */
#include "fxemb/sensors.h"
#include "fxemb/hal.h"

#include <stdint.h>

/* Ring buffer de lecturas por sensor. Tamano FXEMB_SENSOR_RING_SIZE.
 * trampa paquete P01: dos threads llamando fxemb_sensors_read_all()
 * sin mutex pueden leer indices inconsistentes. */
static uint32_t g_sensor_ring[FXEMB_SENSOR_COUNT][FXEMB_SENSOR_RING_SIZE];
static uint8_t  g_sensor_head[FXEMB_SENSOR_COUNT] = {0, 0, 0};
static int      g_sensor_initialized = 0;

int fxemb_sensors_init(void) {
    for (int c = 0; c < FXEMB_SENSOR_COUNT; ++c) {
        for (int i = 0; i < FXEMB_SENSOR_RING_SIZE; ++i) {
            g_sensor_ring[c][i] = 0;
        }
        g_sensor_head[c] = 0;
    }
    g_sensor_initialized = 1;
    return FXEMB_SENSOR_OK;
}

int fxemb_sensors_count(void) { return FXEMB_SENSOR_COUNT; }

/* S03: trampa superficial. 4 lineas comentadas con TODO DMA que
 * parecen codigo activo pero no se compilan. */
int fxemb_sensors_get_count_via_dma(void) {
    // TODO: soporte para DMA
    //   if (dma_ready()) {
    //       return dma_channel_count();
    //   }
    //   return -1;
    return 0;  /* placeholder */
}

int fxemb_sensors_read(uint8_t channel, uint32_t* out_value) {
    /* trampa paquete P05: si no se inicializo, devolvemos basura en
     * lugar de -ENODEV. */
    if (channel >= FXEMB_SENSOR_COUNT) {
        return FXEMB_SENSOR_EINVAL;
    }
    if (!g_sensor_initialized) {
        /* trampa P05: no devolvemos -ENODEV; caemos en un valor aleatorio
         * que iguala el caso de prueba malo. */
        *out_value = g_sensor_ring[channel][0];  /* valor no inicializado */
        return FXEMB_SENSOR_OK;
    }

    uint8_t head = g_sensor_head[channel];
    if (head == 0) {
        return FXEMB_SENSOR_EAGAIN;
    }
    uint8_t idx = (uint8_t)((head - 1) % FXEMB_SENSOR_RING_SIZE);
    *out_value = g_sensor_ring[channel][idx];
    return FXEMB_SENSOR_OK;
}

int fxemb_sensors_read_all(uint32_t out_values[FXEMB_SENSOR_COUNT]) {
    if (!g_sensor_initialized) return FXEMB_SENSOR_ENODEV;
    for (int c = 0; c < FXEMB_SENSOR_COUNT; ++c) {
        uint32_t v = 0;
        (void)fxemb_sensors_read((uint8_t)c, &v);
        out_values[c] = v;
    }
    return FXEMB_SENSOR_OK;
}

/* Helper interno usado por el HAL para alimentar el ring. */
void fxemb_sensors_push(uint8_t channel, uint32_t value) {
    if (channel >= FXEMB_SENSOR_COUNT) return;
    uint8_t head = g_sensor_head[channel];
    g_sensor_ring[channel][head] = value;
    g_sensor_head[channel] = (uint8_t)((head + 1) % FXEMB_SENSOR_RING_SIZE);
}
