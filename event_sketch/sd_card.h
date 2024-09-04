#ifndef _SD_CARD_H
#define _SD_CARD_H

#include <SD_MMC.h>
#include "FS.h"
#include "Arduino.h"

#define SD_MMC_CMD 38  // command
#define SD_MMC_CLK 39  // clock
#define SD_MMC_D0 40   // enable

#define first_comma 0xf0 
#define second_comma 0x0f 

class SD_card{
    private:
    int count = 0;
    File file;
    
    public:
    SD_card()
    {
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

        file = SD_MMC.open("/user02_lab.csv");
        if(!file){
            Serial.println("failed to open file for reading");
            return;
        }
    }

    void get_x_y_value(float &x, float &y){
        char file_char = file.read();
        uint8_t comma = 0x00;
        String file_string = "";

        // seperate the character and convert to numbers 
        while(file_char != '\n'){
            file_char = file.read();
            if(file_char == ','){
                if(!comma){
                    // no comma till now, encountered the first one so, it should be timestamp
                    comma = first_comma;
                }else if(comma == first_comma){
                    x = file_string.toFloat();
                    comma = second_comma;
                }
                file_string = "";
                // file_char = '';
            }else if((file_char == '\n') && (comma == second_comma)){
                y = file_string.toFloat();
                file_string = "";
                // file_char = '';
                comma = 0x00;
            }else{
                file_string += file_char; 
            }
        }
        Serial.printf("idx [%d] -- x : %f, y: %f\n", count, x, y);
        count++;
    }
};


#endif _SD_CARD_H