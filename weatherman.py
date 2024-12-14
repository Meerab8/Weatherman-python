#python3 weatherman.py -e 2001 /home/dev/Desktop/WeatherManApp/lahore_weather
#python3 weatherman.py -a 2002/4 /home/dev/Desktop/WeatherManApp/lahore_weather/lahore_weather_2004_Apr.txt
#python3 weatherman.py -c 2002/4 /home/dev/Desktop/WeatherManApp/lahore_weather/lahore_weather_2004_Apr.txt

import datetime
import sys
import os
from colorama import Fore, Style

option = sys.argv[1]
date = sys.argv[2]
path = sys.argv[3]

class Weather():
  def __init__(self, path, date, option):
    self.path = path
    self.date = date
    self.option = option

  def MaxMinTemperature(self, path,date):
    files = os.listdir(path)
    DataList, MaxTemperatureDate, MinTemperatureDate, MaxHumidityDate, maxTemperatureList, minTemperatureList, maxHumidity = [],[],[],[],[],[],[]
    for f in files:
        currentFilePath = os.path.join(path, f)
        if date in currentFilePath:
          currentfile = open(currentFilePath)
          fileData = currentfile.read()
          fileDataList = fileData.split('\n')[2:-2]
          for data in fileDataList:
            DataList = data.split(',')
            if len(DataList)>1:
              MaxTemperatureDate.append(DataList[0])
              maxTemperatureList.append(DataList[1])
              MinTemperatureDate.append(DataList[0])
              minTemperatureList.append(DataList[3])
              MaxHumidityDate.append(DataList[0])
              maxHumidity.append(DataList[7])

          def removeEmptyStrings(tempList,dateList):
            i=0
            while (i<len(tempList)):
              if ('' == tempList[i]):
                del tempList[i]
                del dateList[i]
              i=i+1

          removeEmptyStrings(maxTemperatureList,MaxTemperatureDate)
          removeEmptyStrings(minTemperatureList,MinTemperatureDate)
          removeEmptyStrings(maxHumidity,MaxHumidityDate)

          def dateformatter(dateValue):
            newDate = list(dateValue.split('-'))
            year,month,day = newDate[0], newDate[1], newDate[2]
            displayDate = datetime.datetime( int(year), int(month), int(day))
            return displayDate.strftime("%B %d")

          def result(temperatureList,operation,dateList):
            intTempList = list(map(int, temperatureList))
            maxValue = operation(intTempList)
            index = intTempList.index(maxValue)
            day = dateList[index]
            dayFormatted = dateformatter(day)
            return (maxValue, dayFormatted )

    MaximumTemperature, MaximumTemperatureDate =result(maxTemperatureList, max, MaxTemperatureDate)
    MinimumTemperature, MinimumTemperatureDate =result(minTemperatureList, min, MinTemperatureDate)
    MaximumHumidity, MaximumHumidityDate =result(maxHumidity, max, MaxHumidityDate)

    print(" Highest: %dC on %s\n Lowest: %dC on %s\n Humid %d%% on %s\n " %(MaximumTemperature, MaximumTemperatureDate, MinimumTemperature, MinimumTemperatureDate, MaximumHumidity, MaximumHumidityDate))

  def AvgTemperature(self, path):
    DataList, AvgTemperatureList, AvgHumidity = [],[],[]

    currentfile = open(path)
    fileData = currentfile.read()
    fileDataList = fileData.split('\n')[2:]
    for data in fileDataList:
      DataList = data.split(',')
      if len(DataList)>1:
        AvgTemperatureList.append(DataList[2])
        AvgHumidity.append(DataList[8])

        def removeEmptyStrings(tempList):
          while('' in tempList):
            tempList.remove('')
    removeEmptyStrings(AvgTemperatureList)
    removeEmptyStrings(AvgHumidity)

    average_temperature_list =  list(map(int, AvgTemperatureList))
    average_humidity_list =  list(map(int, AvgHumidity))

    MaximumAverageTemperature = max(average_temperature_list)
    MinimumAverageTemperature = min(average_temperature_list)
    MaximumAverageHumidity = max(average_humidity_list)
    
    print(" Highest Average: %dC \n Lowest Average: %dC \n Average Humidity %d%% \n " %(MaximumAverageTemperature, MinimumAverageTemperature, MaximumAverageHumidity))

  def coloredTemperatureDisplay(self,path,date):
    DataList = []
    print()

    currentfile = open(path)
    fileData = currentfile.read()
    fileDataList = fileData.split('\n')[2:-2]

    newDate = date.split('/')
    year = newDate[0]
    month = newDate[1]
    displayDate = datetime.datetime(int(year), int(month),1)
    print(displayDate.strftime("%B %Y"))

    i=0
    for data in fileDataList:
      i=i+1
      DataList = data.split(',')
      # print(i, Fore.BLUE+'+'*int(DataList[3]),Style.RESET_ALL,Fore.RED+'+'*int(DataList[1])+ '%sC-' %DataList[3]+'%sC' %DataList[1], Style.RESET_ALL)
      print(i, Fore.RED + '+'*int(DataList[1])+ '%s C' %DataList[1], Style.RESET_ALL)
      print(i, Fore.BLUE + '+'*int(DataList[3])+'%s C' %DataList[3], Style.RESET_ALL)

if option=='-e':
    obj = Weather(path, date,option)
    obj.MaxMinTemperature(path,date)
elif option=='-a':
  obj = Weather(path,date,option)
  obj.AvgTemperature(path)
elif option=='-c':
  obj = Weather(path,date,option)
  obj.coloredTemperatureDisplay(path,date)
else:
  print('Please enter correct option')
