#include <SD_MMC.h>

#include "sd_read_write.h"
#include "sd_card.h"
#include "data_compress.h"

#define SD_MMC_CMD 38  // command
#define SD_MMC_CLK 39  // clock
#define SD_MMC_D0 40   // enable

#define first_comma 0xf0 
#define second_comma 0x0f 

String file_string; 

uint8_t x[10] = {0};
uint8_t y[10] = {0};

void setup() {
    // serial
    Serial.begin(115200);
    SD_card card;

    log_d("Total heap: %d", ESP.getHeapSize());
    log_d("Free heap: %d", ESP.getFreeHeap());
    log_d("Total PSRAM: %d", ESP.getPsramSize());
    log_d("Free PSRAM: %d", ESP.getFreePsram());

    for(int i =0 ; i < 10; i++){
        card.get_x_y_value(x[i], y[i]);
    }

    for(int i = 0 ; i < 5; i++){
        Serial.printf("newe x : %f, y: %f\n", x[i], y[i]);
    }
}

void loop() {
  // put your main code here, to run repeatedly:
}
