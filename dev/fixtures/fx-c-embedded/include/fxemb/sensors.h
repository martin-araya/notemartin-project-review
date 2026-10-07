/* F06y: sensors.h - feature 1: lectura de sensores. */
#ifndef FXEMB_SENSORS_H
#define FXEMB_SENSORS_H

#include <stdint.h>

#define FXEMB_SENSOR_TEMP_CHANNEL   0
#define FXEMB_SENSOR_PRESSURE_CHANNEL 1
#define FXEMB_SENSOR_ACCEL_CHANNEL   2

#define FXEMB_SENSOR_COUNT 3
#define FXEMB_SENSOR_RING_SIZE 8

/* Codigos de retorno (estilo -errno). */
#define FXEMB_SENSOR_OK          0
#define FXEMB_SENSOR_EAGAIN     -11
#define FXEMB_SENSOR_EINVAL     -22
#define FXEMB_SENSOR_ENODEV     -19
#define FXEMB_SENSOR_ERANGE     -34
#define FXEMB_SENSOR_ETIMEDOUT  -110

/* API. */
int  fxemb_sensors_init(void);
int  fxemb_sensors_read(uint8_t channel, uint32_t* out_value);
int  fxemb_sensors_read_all(uint32_t out_values[FXEMB_SENSOR_COUNT]);
int  fxemb_sensors_count(void);

#endif
