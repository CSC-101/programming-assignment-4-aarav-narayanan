from build_data import get_data
from data import CountyDemographics
#THis program will display the data from the county demographics with each print line showing the contents.
#Input is the demographics created from loading the file
#Output is the contents of what is going to be displayed.
def display_data(demographics):
    for county in demographics: #For loop to check each county in the demographics list
        print("County:",county.county) #Print for each contents for all of them and for population it will be for 2014
        print("State:",county.state)
        print("Population: ",county.population['2014 Population'])
        print("Education: ",county.education)
        print("Ethnicity: ",county.ethnicities)
        print("Income: ",county.income)
        print("-"*10)
#Purpose of the function is to filter the data to only contain data with a specific state abbriviation
#Input is the demographics and the state abbreviation while output is the data from demographics containing that specific abbriviation
def filter_state(demographics,state_abbrv):
    fiter_list=[] #empty list
    for i in demographics: #for loop to check each one
        if i.state==state_abbrv: #see if it is the same state abbriviation
            fiter_list.append(i) #Append to the list
    print("Filter state = ",state_abbrv) #print out the abbriviate
    print(len(fiter_list),"entries")  #Show how many entries were entered
    return fiter_list
#Purpose is to reduce the data by showing is a certain field (education) is higher than a certain threshold value
#Input is the demographics, the field such as education and the threshold value as a number
#Output is the dats being reduced if the contents in the field is greater than the threshold value
def filter_gt(demographics,field,threshold):
    filter_list=[] #empty list
    for county in demographics: #for loop to check each county in the demographics
        field_parts=field.split('.') #Split between the field name and its contents such as Education.Bachelor's Degree or Higher
        if "Education" in field: #Check if this certain key is the field and if so check if the value is greater than the threshold
            if county.education[field_parts[1]]>threshold:
                filter_list.append(county)
        elif "Ethnicities" in field: #THe same will be check for the other field values
            if county.ethnicities[field_parts[1]]>threshold:
                filter_list.append(county)
        elif "Income" in field:
            if county.income[field_parts[1]]>threshold:
                filter_list.append(county)
    print("Filter:",field, "gt",threshold,(len(filter_list),"entries")) #print to the terminal of the list of cunties with this specific information
    return filter_list

#Purpose is to reduce the data by showing is a certain field (education) is less than a certain threshold value
#Input is the demographics, the field such as education and the threshold value as a number
#Output is the dats being reduced if the contents in the field is less than the threshold value
def filter_lt(demographics,field,threshold):
    filter_list=[] #empty list
    for county in demographics:
        field_parts=field.split('.') #Split between the field name and its contents such as Education.Bachelor's Degree or Higher
        if "Education" in field:
            if county.education[field_parts[1]]<threshold: #Check if this certain key is the field and if so check if the value is less than the threshold
                filter_list.append(county)
        elif "Ethnicities" in field: #THe same will be checked for the other field values
            if county.ethnicities[field_parts[1]]<threshold:
                filter_list.append(county)
        elif "Income" in field:
            if county.income[field_parts[1]]<threshold:
                filter_list.append(county)
    print("Filter:",field, "lt",threshold,(len(filter_list),"entries")) #print to the terminal of the list of counties with this specific information
    return filter_list
#Purpose is to find the total population within the 2014 for each county in demographics
#Input is the demographics with the CountyDemographics class
#Output is the addition of the 2014 populations from all counties
def population_total(demographics):
    add=0 #Start off with 0
    for county in demographics: #For loop to go through each county
        add+=county.population['2014 Population'] #Add in the 2014 population from each county
    return add
#Purpose is to gather the sub_population for each field within the 2014 population
#Input is the demographics fromm the class and the other is the field
#Output is the total sub_population calculation for the field being used
def population_field(demographics, field)->list[CountyDemographics]:
    add=0 #start off with 0
    field_sep=field.split(".")
    for county in demographics: #Check each one in the demographics list
        if field_sep[0]=="Education": #Check if the field is within the class
            add+=county.population["2014 Population"] * (county.education[field_sep[1]] / 100)
            #Calculate the sub_population by
            # converting the percentage of the field into a decimal and multiply by the 2014 population
            #The same can be said for the other fields which is why they are an elif statement
        elif field_sep[0]=="Ethnicities":
            add += county.population["2014 Population"] * (county.ethnicities[field_sep[1]] / 100)
        elif field_sep[0]=="Income":
            add += county.population['2014 Population']*(county.income[field_sep[1]]/100)
     #Print to the terminal by starting off with 2014 and then the field and the number
    return add
#Purpose is to get a percentage by calculating the sub and total population from previous functions
#Input is the demographics list and the field attached to that and the output is  the percentage calculated from the input
def percent(demographics,field):
    total_pop = population_total(demographics) #Get the total population using the demographics list
    sub_pop= population_field(demographics,field) #Get the sub_population from the demographics list and  the field
    if sub_pop!=0 and total_pop!=0: #To show if 0 is not the answer then it can go ahead with the percent calculation
        field_percent=100 * (sub_pop/total_pop)#Find the percentage by dividing sub_pop/pop_total times 100
    else:
        return 0
    print("2014",field,field_percent) #Printing to the terminal by showing the field and the percentage
    return field_percent
#THe purpose of this function is to check if each operation file can be used in the previous functions
#Input is the demographics from the data and the operation files
#Output is whatever the previous function's output will be if the key is correct
def execute_operations(demographics,operations):
    line_num=1 #Check each line so that whatever line will be used in the exception
    for i in operations: #for loop to check each line in the operations
        split_ops=i.split(':') #Split it up to see if the first key will be used
        if len(split_ops)>3: #If there are more than 3 index then it will be an error
            print("Error: invalid file since it got split too many times")
        try:
            if split_ops[0]=='display': #Try place to check if the first index is the right key and it will call out the functions
                display_data(demographics)
            elif split_ops[0]=='filter-state':
                demographics=filter_state(demographics,split_ops[1])
            elif split_ops[0]=='filter-gt':
                demographics=filter_gt(demographics,split_ops[1],float(split_ops[2]))
            elif split_ops[0]=='filter-lt':
                demographics = filter_lt(demographics, split_ops[1], float(split_ops[2]))
            elif split_ops[0]=='population-total':
                print("2014 population:",population_total(demographics)) #to print out the population total
            elif split_ops[0]=='population':
                print("2014", split_ops[1], "population", population_field(demographics,split_ops[1])) #to print out the population field
            elif split_ops[0]=='percent':
                percent(demographics,split_ops[1])
            else:
                print("Invalid key used")
        except ValueError:
            print("Error: There is no number entered in line ", line_num)
        except IndexError:
            print("Error: Unsupported on line: ",line_num)
        except KeyError:
            print("Key Not Correctly Used on line: ",line_num)
        line_num+=1
#Main function to test it out
if __name__=='__main__':
    data=get_data()
    files_list=["inputs/bachelors_gt_60.ops","inputs/ca.ops","inputs/filter_state.ops",
            "inputs/high_school_lt_60.ops","inputs/percent_fields.ops","inputs/pop.ops",
            "inputs/pop_field.ops","inputs/some_errors.ops",
                "task2_a.ops","task2_b.ops","task2_c.ops","task2_d.ops"] #List of all operation files
    list_num=int(input("Enter a number from 0-11 to check each tasks: ")) #Input number that will be based on the list
    try:
        with open(files_list[list_num],'r')as file: #Callos out the file according to the number inputted by the user
            print(len(data),"records loaded") #Show how many records
            operations=[line.strip() for line in file if line.strip()] #To separate the operations as a list
            execute_operations(data,operations) #Call out the function that will call out the other functions
    except FileNotFoundError: #Error if file not found
        print("Error: File Not Found")
    except IOError as e: #Error if unable to read data
        print("Error:",e)











