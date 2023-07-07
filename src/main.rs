#![deny(unsafe_code)]
#![allow(clippy::empty_loop)]
#![no_main]
#![no_std]

use crate::hal::{pac, prelude::*};
use cortex_m_rt::entry;
use panic_halt as _;
use stm32f4xx_hal as hal;

#[entry]
fn main() -> ! {
    if let (Some(dp), Some(cp)) = (
        pac::Peripherals::take(),
        cortex_m::peripheral::Peripherals::take(),
    ) {
        // Set up the system clock
        // let rcc = dp.RCC.constrain();
        // let clocks = rcc
        //     .cfgr
        //     .use_hse(25.MHz())
        //     .sysclk(100.MHz())
        //     .hclk(25.MHz())
        //     .freeze();

        // LED on Black Pill is on pin C13
        let gpioc = dp.GPIOC.split();
        let mut led = gpioc.pc13.into_push_pull_output();

        // Delay provider
        // let mut delay = cp.SYST.delay(&clocks);

        led.set_low();
        // delay.delay_ms(2000_u32);

        // loop {
        //     led.set_high();
        //     delay.delay_ms(1000_u32);
        //     led.set_low();
        // }
    }

    loop {}
}
