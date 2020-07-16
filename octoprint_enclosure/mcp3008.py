import ctypes
import struct
import sys
import spidev

# Raspberry Pi hardware SPI configuration.
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):

  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  388       75    1.25
  #  465      100    1.50
  #  543      125    1.75
  #  620      150    2.00
  #  698      175    2.25
  #  775      200    2.50
  #  853      225    2.75
  #  930      250    3.00
  # 1008      275    3.25
  # 1023      280    3.30

  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

def main():
    # Get bus address if provided or use default address
    SPI_CHANNEL = 0
    if len(sys.argv) >= 2:
        SPI_CHANNEL = int(sys.argv[1], 0)

    if not 0 <= SPI_CHANNEL <= 7:
        raise ValueError("Invalid channel")

    # Define sensor channels

    temp_level = ReadChannel(SPI_CHANNEL)
    temp_volts = ConvertVolts(temp_level,2)
    temp       = ConvertTemp(temp_level,2)

    print('{0:0.1f}'.format(temp))

if __name__ == "__main__":
    main()
