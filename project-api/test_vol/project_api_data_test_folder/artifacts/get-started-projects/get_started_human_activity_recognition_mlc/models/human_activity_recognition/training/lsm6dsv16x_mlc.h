     
/**
******************************************************************************
* @attention
*
* Copyright (c) 2024 STMicroelectronics.
* All rights reserved.
*
* This software is licensed under terms that can be found in the LICENSE file
* in the root directory of this software component.
* If no LICENSE file comes with this software, it is provided AS-IS.
*
******************************************************************************
*/

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef MLC_CONFIGURATION_H
#define MLC_CONFIGURATION_H

#ifdef __cplusplus
    extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#ifndef MEMS_UCF_SHARED_TYPES
#define MEMS_UCF_SHARED_TYPES

/** Common data block definition **/
typedef struct {
    uint8_t address;
    uint8_t data;
} ucf_line_t;

#endif /* MEMS_UCF_SHARED_TYPES */

/** Configuration array generated from Unico Tool **/
static const ucf_line_t mlc_configuration[] = {
	{.address = 0x10, .data = 0x00,},
	{.address = 0x11, .data = 0x00,},
	{.address = 0x01, .data = 0x80,},
	{.address = 0x04, .data = 0x00,},
	{.address = 0x05, .data = 0x00,},
	{.address = 0x17, .data = 0x40,},
	{.address = 0x02, .data = 0x11,},
	{.address = 0x08, .data = 0xE8,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x3C,},
	{.address = 0x02, .data = 0x11,},
	{.address = 0x08, .data = 0xF1,},
	{.address = 0x09, .data = 0x01,},
	{.address = 0x02, .data = 0x21,},
	{.address = 0x08, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x02, .data = 0x11,},
	{.address = 0x08, .data = 0xEA,},
	{.address = 0x09, .data = 0xC2,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0xCE,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x0A,},
	{.address = 0x02, .data = 0x11,},
	{.address = 0x08, .data = 0xF2,},
	{.address = 0x09, .data = 0x50,},
	{.address = 0x02, .data = 0x11,},
	{.address = 0x08, .data = 0xFA,},
	{.address = 0x09, .data = 0x5C,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0xEC,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0xF8,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x02, .data = 0x31,},
	{.address = 0x08, .data = 0x5C,},
	{.address = 0x09, .data = 0x0D,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x93,},
	{.address = 0x09, .data = 0x28,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x93,},
	{.address = 0x09, .data = 0xA8,},
	{.address = 0x09, .data = 0x51,},
	{.address = 0x09, .data = 0xBF,},
	{.address = 0x09, .data = 0x6E,},
	{.address = 0x09, .data = 0x3B,},
	{.address = 0x09, .data = 0x3F,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x11,},
	{.address = 0x09, .data = 0x08,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x08,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x90,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x10,},
	{.address = 0x09, .data = 0x08,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0x04,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x02,},
	{.address = 0x09, .data = 0x08,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x01,},
	{.address = 0x09, .data = 0x04,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x11,},
	{.address = 0x09, .data = 0x04,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x10,},
	{.address = 0x09, .data = 0x04,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x10,},
	{.address = 0x09, .data = 0x90,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x01,},
	{.address = 0x09, .data = 0x98,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x02,},
	{.address = 0x09, .data = 0x98,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x03,},
	{.address = 0x09, .data = 0x98,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x11,},
	{.address = 0x09, .data = 0x98,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x10,},
	{.address = 0x09, .data = 0x98,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0xFC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x7C,},
	{.address = 0x09, .data = 0x1F,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x02, .data = 0x31,},
	{.address = 0x08, .data = 0xEC,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x09, .data = 0x00,},
	{.address = 0x01, .data = 0x00,},
	{.address = 0x01, .data = 0x80,},
	{.address = 0x17, .data = 0x40,},
	{.address = 0x02, .data = 0x31,},
	{.address = 0x08, .data = 0xF8,},
	{.address = 0x09, .data = 0x23,},
	{.address = 0x09, .data = 0x3C,},
	{.address = 0x09, .data = 0x02,},
	{.address = 0x09, .data = 0x80,},
	{.address = 0x09, .data = 0x51,},
	{.address = 0x09, .data = 0x30,},
	{.address = 0x09, .data = 0x40,},
	{.address = 0x09, .data = 0xE0,},
	{.address = 0x02, .data = 0x41,},
	{.address = 0x08, .data = 0x00,},
	{.address = 0x09, .data = 0x62,},
	{.address = 0x09, .data = 0x3C,},
	{.address = 0x09, .data = 0x8C,},
	{.address = 0x09, .data = 0xE2,},
	{.address = 0x01, .data = 0x80,},
	{.address = 0x17, .data = 0x00,},
	{.address = 0x04, .data = 0x00,},
	{.address = 0x05, .data = 0x10,},
	{.address = 0x02, .data = 0x01,},
	{.address = 0x01, .data = 0x00,},
	{.address = 0x5E, .data = 0x02,},
	{.address = 0x01, .data = 0x80,},
	{.address = 0x0D, .data = 0x01,},
	{.address = 0x60, .data = 0x15,},
	{.address = 0x45, .data = 0x02,},
	{.address = 0x01, .data = 0x00,},
	{.address = 0x10, .data = 0x04,},
	{.address = 0x11, .data = 0x00,},
	{.address = 0x15, .data = 0x00,},
	{.address = 0x17, .data = 0x01,}
};

#ifdef __cplusplus
}
#endif

#endif /* MLC_CONFIGURATION_H */
    