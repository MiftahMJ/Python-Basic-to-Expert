# # with open("weather_data(in).csv") as data:
# #     data1= data.readlines()
# #     print(data1)
#
# # import csv
# # with open("weather_data(in).csv") as data:
# #     data1=csv.reader(data)
# #     temperatures=[]
# #     for row in data1:
# #        if row[1]!="temp":
# #            temperatures.append(row[1])
# #            print(temperatures)
# import pandas
# data=pandas.read_csv("weather_data(in).csv")
# # print(type(data["temp"]))
# # data_dict=data.to_dict()
# # print(data_dict)
# #
# # temp_list=data["temp"].to_list()
# # print(len(temp_list))
# # print(data["temp"].mean())
# # print(data["temp"].max())
# #
# # # data columns
# # print(data["condition"])
# # print(data.condition)
# # data in rows
# # print(data[data.day=="Monday"])
# # print(data[data.temp == data.temp.max()])
# # moday= data[data.day=="Monday"]
# # print(moday.condition)
#
#
#  # create dataframe from scratch#
# data_dict={
#      "students":["amy","james","miftah"],
#      "scores":[76,90,99]
#  }
# data1=pandas.DataFrame(data_dict)
# print(data)
# data.to_csv("new_data.csv")


import pandas
data= pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
grey_squirrels_count=len(data[data["Primary Fur Color"]=="Gray"])
red_squirrels_count=len(data[data["Primary Fur Color"]=="Cinnamon"])
black_squirrels_count=len(data[data["Primary Fur Color"]=="Black"])

print(grey_squirrels_count)
print(red_squirrels_count)
print(black_squirrels_count)
data_dict={
    "Fur Color":["Gray","Cinnamon","Black"],
    "Count":[grey_squirrels_count,red_squirrels_count,black_squirrels_count]
}
df=pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")
