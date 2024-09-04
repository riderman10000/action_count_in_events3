#include <SD_MMC.h>

#include "sd_read_write.h"
#include "data_compress.h"

#define SD_MMC_CMD 38  // command
#define SD_MMC_CLK 39  // clock
#define SD_MMC_D0 40   // enable

#define first_comma 0xf0 
#define second_comma 0x0f 

float x[16000] = {0};
float y[16000] = {0};

String file_string; 

void get_x_y(float &x, float &y){

}

void setup() {
    // serial
    Serial.begin(115200);

    // SD_MMC setup
    SD_MMC.setPins(SD_MMC_CLK, SD_MMC_CMD, SD_MMC_D0);
    if (!SD_MMC.begin("/sdcard", true, true, SDMMC_FREQ_DEFAULT, 5)) {
        Serial.println("Card Mount Failed!");
        return;
    }
    uint8_t cardType = SD_MMC.cardType();
    if (cardType == CARD_NONE) {
        Serial.println("No SD_MMC card attached");
        return;
    }

    Serial.print("SD_MMC Card Type: ");
    if (cardType == CARD_MMC) {
        Serial.println("MMC");
    } else if (cardType == CARD_SD) {
        Serial.println("SDSC");
    } else if (cardType == CARD_SDHC) {
        Serial.println("SDHC");
    } else {
        Serial.println("UNKNOWN");
    }
    uint64_t cardSize = SD_MMC.cardSize() / (1024 * 1024);
    Serial.printf("SD_MMC Card Size: %lluMB\n", cardSize);

    listDir(SD_MMC, "/", 0);

    File file = SD_MMC.open("/user02_lab.csv");
    if(!file){
        Serial.println("failed to open file for reading");
        return;
    }
    Serial.println("reading from file: ");
    for(int i =0 ; i < 10; i++){
        char file_char = file.read();
        uint8_t comma = 0x00; // 0xf0; // first comma , 0x0f second comma
        file_string = "";

        // seperate the character and convert to numbers 
        while(file_char != '\n'){
            file_char = file.read();
            if(file_char == ','){
                if(!comma){
                    // no comma till now, encountered the first one so, it should be timestamp
                    comma = first_comma;
                }else if(comma == first_comma){
                    x[i] = file_string.toFloat();
                    comma = second_comma;
                }
                file_string = "";
                // file_char = '';
            }else if((file_char == '\n') && (comma == second_comma)){
                y[i] = file_string.toFloat();
                file_string = "";
                // file_char = '';
                comma = 0x00;
            }else{
                file_string += file_char; 
            }

        }
        Serial.printf("x : %f, y: %f\n", x[i], y[i]);
    }
}

void loop() {
  // put your main code here, to run repeatedly:
}
