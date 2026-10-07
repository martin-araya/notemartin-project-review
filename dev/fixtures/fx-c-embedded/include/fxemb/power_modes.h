/* F06y: power_modes.h - feature 3: modos de bajo consumo. */
#ifndef FXEMB_POWER_MODES_H
#define FXEMB_POWER_MODES_H

typedef enum {
    FXEMB_POWER_RUN     = 0,
    FXEMB_POWER_IDLE    = 1,
    FXEMB_POWER_SLEEP   = 2,
    FXEMB_POWER_DEEPSLEEP = 3,
} fxemb_power_mode_t;

typedef enum {
    FXEMB_WAKEUP_NONE   = 0,
    FXEMB_WAKEUP_GPIO   = 1,
    FXEMB_WAKEUP_RTC    = 2,
    FXEMB_WAKEUP_WATCHDOG = 3,
} fxemb_wakeup_source_t;

int  fxemb_power_init(void);
int  fxemb_power_enter(fxemb_power_mode_t mode, fxemb_wakeup_source_t wakeup);
int  fxemb_power_current_mode(void);
int  fxemb_power_wakeup_pending(void);
int  fxemb_power_clear_wakeup(void);
int  fxemb_power_consumption_ua(void);

#endif
