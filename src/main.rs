#![allow(clippy::empty_loop)]
#![no_main]
#![no_std]

use cortex_m_rt::entry;
use keyberon::key_code::KeyCode;
use panic_halt as _;
use rtt_target::{rprintln, rtt_init_print};
use stm32f4xx_hal::{
    adc::{
        config::{AdcConfig, SampleTime},
        Adc,
    },
    gpio::{Output, Pin},
    pac,
    prelude::*,
};

const DIGITAL: bool = true;
const THRESHOLD: u16 = 4;

fn write_bits(mut n: u8, buf: &mut [u8]) {
    (0..4).for_each(|i| {
        buf[i] = n & 1;
        n >>= 1;
    });
}

fn set_channel(
    n: u8,
    select: &mut (
        Pin<'C', 14, Output>,
        Pin<'B', 8, Output>,
        Pin<'B', 12, Output>,
        Pin<'A', 15, Output>,
    ),
) {
    if n > 15 {
        panic!("Requested channel number too great!")
    }

    let mut n_bits = [0; 4];
    write_bits(n, &mut n_bits);

    n_bits.iter().enumerate().for_each(|(i, &bit)| match i {
        0 => {
            if bit == 0 {
                select.0.set_low();
            } else {
                select.0.set_high();
            }
        }
        1 => {
            if bit == 0 {
                select.1.set_low();
            } else {
                select.1.set_high();
            }
        }
        2 => {
            if bit == 0 {
                select.2.set_low();
            } else {
                select.2.set_high();
            }
        }
        3 => {
            if bit == 0 {
                select.3.set_low();
            } else {
                select.3.set_high();
            }
        }
        _ => panic!("This should never happen!"),
    });
}

#[entry]
fn main() -> ! {
    if let Some(dp) = pac::Peripherals::take() {
        rtt_init_print!();

        let gpioa = dp.GPIOA.split();
        let gpiob = dp.GPIOB.split();
        let gpioc = dp.GPIOC.split();

        let mut select = (
            gpioc.pc14.into_push_pull_output(),
            gpiob.pb8.into_push_pull_output(),
            gpiob.pb12.into_push_pull_output(),
            gpioa.pa15.into_push_pull_output(),
        );

        let mut led = gpioc
            .pc13
            .into_push_pull_output_in_state(stm32f4xx_hal::gpio::PinState::High);

        let mut adc = Adc::adc1(dp.ADC1, true, AdcConfig::default());

        let am0_pin = gpioa.pa1.into_analog();
        let am1_pin = gpioa.pa2.into_analog();

        let am0_codes = [
            Some(KeyCode::Kp0),
            Some(KeyCode::Kp1),
            Some(KeyCode::Kp4),
            None,
            None,
            None,
            Some(KeyCode::Kp7),
            Some(KeyCode::NumLock),
            Some(KeyCode::KpSlash),
            Some(KeyCode::Kp8),
            None,
            None,
            None,
            None,
            Some(KeyCode::Kp5),
            Some(KeyCode::Kp2),
        ];

        let am1_codes = [
            Some(KeyCode::KpDot),
            Some(KeyCode::Kp3),
            Some(KeyCode::Kp6),
            None,
            None,
            None,
            Some(KeyCode::Kp9),
            Some(KeyCode::KpAsterisk),
            Some(KeyCode::KpMinus),
            None,
            None,
            None,
            None,
            None,
            Some(KeyCode::KpPlus),
            Some(KeyCode::KpEnter),
        ];

        if DIGITAL {
            loop {
                set_channel(0, &mut select);
                let reading = adc.convert(&am0_pin, SampleTime::Cycles_3) / 4;
                rprintln!("{}", reading);

                // for i in 0..16 {
                //     set_channel(i as u8, &mut select);
                //     if am0_codes[i].is_some() {
                //         let delta = (am0_resting_values[i].unwrap()
                //             - adc.convert(&am0_pin, SampleTime::Cycles_112) as i32)
                //             .abs();

                //         if delta >= DIGITAL_CONFIG.threshold {
                //             let mut erroneous = false;

                //             for _ in 0..DIGITAL_CONFIG.tests {
                //                 let delta = (am0_resting_values[i].unwrap()
                //                     - adc.convert(&am0_pin, SampleTime::Cycles_112) as i32)
                //                     .abs();
                //                 if delta < DIGITAL_CONFIG.threshold {
                //                     erroneous = true;
                //                 }
                //             }

                //             if !erroneous {
                //                 rprintln!("\x1b[0;31m{:?} pressed\x1b[39m", am0_codes[i].unwrap());
                //             }
                //         }
                //     }

                //     if am1_codes[i].is_some() {
                //         let delta = (am1_resting_values[i].unwrap()
                //             - adc.convert(&am1_pin, SampleTime::Cycles_112) as i32)
                //             .abs();

                //         if delta >= DIGITAL_CONFIG.threshold {
                //             let mut erroneous = false;

                //             for _ in 0..DIGITAL_CONFIG.tests {
                //                 let delta = (am1_resting_values[i].unwrap()
                //                     - adc.convert(&am1_pin, SampleTime::Cycles_112) as i32)
                //                     .abs();
                //                 if delta < DIGITAL_CONFIG.threshold {
                //                     erroneous = true;
                //                 }
                //             }

                //             if !erroneous {
                //                 rprintln!("\x1b[0;31m{:?} pressed\x1b[39m", am1_codes[i].unwrap());
                //             }
                //         }
                //     }
                // }
            }
        }
    }

    loop {}
}
