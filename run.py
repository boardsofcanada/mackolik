from mackolik import Mackolik

file_name= input("Enter file name: ")
print("Date format: 01/01/2018")
start_date = input("Enter start date: ")
end_date = input("Enter end date (If None, just enter): ")

m = Mackolik(file_name, start_date, end_date)
m.main()
