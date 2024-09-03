#include <SD_MMC.h>
#include "sd_read_write.h"

#define SD_MMC_CMD 38 // command
#define SD_MMC_CLK 39 // clock 
#define SD_MMC_D0  40 // enable 

void setup() {
  // serial 
  Serial.begin(115200);

  // SD_MMC setup
  SD_MMC.setPins(SD_MMC_CLK, SD_MMC_CMD, SD_MMC_D0);
  if(!SD_MMC.begin("/sdcard", true, true, SDMMC_FREQ_DEFAULT, 5)){
    Serial.println("Card Mount Failed!");
    return;
  }
  unit8_t cardType = SD_MMC.cardType();
}

void loop() {
  // put your main code here, to run repeatedly:
}
