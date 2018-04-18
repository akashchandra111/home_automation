#include <SoftwareSerial.h>

const int RX = 0;
const int TX = 1;

// Digital Pins are: 2, 4, 7, 8. 12, 13
// PWM Pins are: 3, 5, 6, 9, 10, 11
const int d_pin[6] = {2, 4, 7, 8, 12, 13};
const int p_pin[6] = {3, 5, 6, 9, 10, 11};

short flag = 0;
char c;

char command;
int intensity;
int pin_no;

String temp1;

bool is_dpin = false;

// Initializing the BT serial object
SoftwareSerial BT(RX, TX);

// Command parser
void run_command(int pin_no, int intensity) {
  if (pin_no < 2 && pin_no > 13) {
    BT.println("Error!");
  }
  else  {
    if (intensity < 0) {
      intensity = 0;
    }
    else if (intensity > 100)  {
      intensity = 100;
    }
    else;

    for (int i = 0; i < 6; i++) {
      if (pin_no == d_pin[i]) {
        is_dpin = true;
        break;
      }
    }

    if (is_dpin == true) {
      if (intensity == 0)  {
        digitalWrite(pin_no, LOW);
      }
      else  {
        digitalWrite(pin_no, HIGH);
      }
      is_dpin = false;
      return;
    }
    else  {
      analogWrite(pin_no, map(intensity, 0, 100, 0, 255));
      return;
    }
  }
}

void setup() {
  BT.begin(9600);

  // Initializing all pins
  for (int i = 0; i < 6; i++) {
    pinMode(d_pin[i], OUTPUT);
    pinMode(p_pin[i], OUTPUT);
  }
}

void loop() {

  if (BT.available() > 0) {
    while (BT.available())  {
      delay(30);
      c = BT.read();
      temp1 += c;
    }
    flag = 1;
  }


  if (flag == 1)  {
    // Command should be in format of "12 255"
    // Which means
    // 12: Pin Number
    // 255: Value

    // BT.println("Data");
    pin_no = temp1.substring(0, temp1.indexOf(' ')).toInt();
    // BT.println(pin_no);
    intensity = temp1.substring(temp1.indexOf(' ') + 1).toInt();
    // BT.println(intensity);

    run_command(pin_no, intensity);
    BT.println("Done !");
    
    flag = 0;
    temp1 = "";
    pin_no = 999;
    intensity = 999;
  }
}
