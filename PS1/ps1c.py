# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 18:54:12 2024

@author: abcde
"""
#variables initialization
annual_salary=0.0   #for a year
portion_saved=0.0   #for a month  
steps_num=0         #number of steps to get correct answer

annual_salary=float(input("Enter your annual salary: "))
current_salary=annual_salary
portion_saved_low=0
portion_saved_high=10000
total_cost=1000000
semi_annual_rise=0.07
portion_saved=int((portion_saved_low+portion_saved_high)/2)
current_savings=0.0

for month_num in range(1,37):
    current_savings+=(current_savings*0.04)/12
    current_savings+=(current_salary*portion_saved_high)/120000
    if(month_num%6==0):
        current_salary+=semi_annual_rise*current_salary
#print(total_cost*0.25)
#print(current_savings,portion_saved_high)

if current_savings<total_cost*0.25:
    print("It is not possible to pay the down payment in three years.")
else: 
    current_savings=0.0
    current_salary=annual_salary
    for month_num in range(1,37):
        current_savings+=(current_savings*0.04)/12
        current_savings+=(current_salary*portion_saved)/120000
        if(month_num%6==0):
            current_salary+=semi_annual_rise*current_salary
    #print(current_savings)
    while abs(current_savings-total_cost*0.25) >= 100:
        if current_savings < total_cost*0.25 :
            portion_saved_low = portion_saved
        else:
            portion_saved_high = portion_saved
        portion_saved = int((portion_saved_high+portion_saved_low)/2)
        current_savings=0.0
        current_salary=annual_salary
        for month_num in range(1,37):
            current_savings+=(current_savings*0.04)/12
            current_savings+=current_salary*(portion_saved/10000)/12
            if(month_num%6==0):
                current_salary+=semi_annual_rise*current_salary
        #print(current_savings)
        #if steps_num<10:
        #print(current_savings,portion_saved)
        steps_num+=1
    print("Best savings rate:",portion_saved/10000)
    print("Steps in bisection search:",steps_num)



#month_num=0
#current_savings=0.0
#current_salary=150000
#semi_annual_rise=0.07
#portion_saved=4411
#while current_savings < (total_cost*0.25):
    #current_savings+=(current_savings*0.04)/12
    #current_savings+=current_salary*(portion_saved/10000)/12
    #month_num+=1
    #if(month_num%6==0):
        #current_salary+=semi_annual_rise*current_salary
#print("Number of months:",month_num)
#print("Current savings:",current_savings)