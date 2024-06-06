# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 18:54:12 2024

@author: abcde
"""
#variables initialization
annual_salary=0.0   #for a year
portion_saved=0.0   #for a month
total_cost=0.0      
portion_down_payment=0.0
current_savings=0.0
semi_annual_rise=0.0
month_num=0

annual_salary=float(input("Enter your annual salary: "))
portion_saved=float("0"+input("Enter the percent of your salary to save, as a decimal: "))
total_cost=float(input("Enter the cost of your dream home: "))
semi_annual_rise=float("0"+input("Enter the semiannual raise, as a decimal: "))
while current_savings < (total_cost*0.25):
    current_savings+=(current_savings*0.04)/12
    current_savings+=annual_salary*portion_saved/12
    month_num+=1
    if(month_num%6==0):
        annual_salary+=semi_annual_rise*annual_salary
print("Number of months:",month_num)