/* Bench A planning contract; not a hardware driver or firmware binary.
 * Sources: STM32F072 DS9826 Rev 6; INA228 SLYS021A.
 * Pin numbers refer to STM32F072CBT6 LQFP48.
 */
#ifndef POWER_WIDGET_BOARD_CONTRACT_H
#define POWER_WIDGET_BOARD_CONTRACT_H

#include <stdint.h>

#define PW_BOARD_REVISION "A-DRAFT"
#define PW_MCU_PART "STM32F072CBT6"
#define PW_CPU_HZ UINT32_C(48000000)
#define PW_I2C_HZ UINT32_C(100000)
#define PW_REPORT_US UINT32_C(1000000)
#define PW_INA_WINDOW_NOMINAL_US UINT32_C(17280)
#define PW_SHUNT_NOMINAL_UOHM UINT32_C(5000)

/* GPIO port letter, bit and physical pin; peripheral selection is in README. */
#define PW_VBUS_GPIO 'A'
#define PW_VBUS_BIT 0u
#define PW_VBUS_PIN 10u
#define PW_ISO_ENABLE_GPIO 'A'
#define PW_ISO_ENABLE_BIT 1u
#define PW_ISO_ENABLE_PIN 11u
#define PW_I2C_GPIO 'B'
#define PW_I2C_SCL_BIT 6u
#define PW_I2C_SCL_PIN 42u
#define PW_I2C_SDA_BIT 7u
#define PW_I2C_SDA_PIN 43u
#define PW_I2C_AF 1u
#define PW_UART_GPIO 'A'
#define PW_UART_TX_BIT 2u
#define PW_UART_TX_PIN 12u
#define PW_UART_RX_BIT 3u
#define PW_UART_RX_PIN 13u
#define PW_UART_AF 1u
#define PW_USB_DM_PIN 32u
#define PW_USB_DP_PIN 33u
#define PW_SWDIO_PIN 34u
#define PW_SWCLK_PIN 37u
#define PW_USER_BUTTON_PIN 18u
#define PW_ACTIVITY_LED_PIN 19u

#define PW_INA_ADDR_7BIT 0x40u
#define PW_INA_REG_CONFIG 0x00u
#define PW_INA_REG_ADC_CONFIG 0x01u
#define PW_INA_REG_SHUNT_CAL 0x02u
#define PW_INA_REG_VSHUNT 0x04u
#define PW_INA_REG_VBUS 0x05u
#define PW_INA_REG_DIAG_ALRT 0x0bu
#define PW_INA_REG_MANUFACTURER_ID 0x3eu
#define PW_INA_REG_DEVICE_ID 0x3fu

/* ADCRANGE=0: +/-163.84 mV. No die-temperature shunt compensation. */
#define PW_INA_CONFIG 0x0000u
/* Continuous shunt+bus, 540 us each, temperature disabled, 16 averages. */
#define PW_INA_ADC_LOGGING 0xb922u
/* Diagnostic only: 1052 us each, 256 averages (AVG code 5, not 6). */
#define PW_INA_ADC_PRECISION 0xbb6du
/* ALATCH=1 makes the conversion-ready status clear on read; ALERT unused. */
#define PW_INA_DIAG_CONFIG 0x8000u
#define PW_INA_DIAG_READY 0x0002u
#define PW_INA_DIAG_MEMORY_OK 0x0001u
#define PW_INA_DIAG_MATH_OVERFLOW 0x0200u

/* Both data registers are three bytes, MSB first, with data in bits 23:4.
 * Keep calibrated calculations at greater precision than output units.
 * Wide-range shunt LSB = 312.5 nV; bus LSB = 195.3125 uV.
 * Gain/offset calibration is additional, and not implemented in this header.
 */
static inline uint32_t pw_unpack_u20(const uint8_t bytes[3]) {
    return ((uint32_t)bytes[0] << 12) |
           ((uint32_t)bytes[1] << 4) | ((uint32_t)bytes[2] >> 4);
}
static inline int32_t pw_unpack_s20(const uint8_t bytes[3]) {
    uint32_t raw = pw_unpack_u20(bytes);
    return (raw & UINT32_C(0x80000)) ?
           (int32_t)raw - INT32_C(1048576) : (int32_t)raw;
}

#endif
