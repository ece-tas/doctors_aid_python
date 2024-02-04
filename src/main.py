class FileOperations:
    @staticmethod
    def writeFile(x, y = None):
        with open('doctors_aid_outputs.txt', 'a') as o:  # opening output file
            if y is not None:
                o.writelines(y)
            o.write(x)      # writing preparations into output file
            o.close()

    def openFile(file):
        with open(file,"r") as f:       # reading text from the input file
            global inputs
            inputs = f.readlines()            # reading line by line
            f.close()

    """ def writeList(*args):           # unrestricted function for variable number of arguments
        with open('doctors_aid_outputs.txt', 'a') as o:
            o.write("".join(map(str, args))) """

# Read input data from file
FileOperations.openFile("src//doctors_aid_inputs.txt")
matrix = []
patient_data_list = []
patient_names = []

# Populate matrix with input data
for text in inputs:         # make text into list in list
    each_line_list = text.split(", ")     # separating lines from "," and "a space"
    matrix.append([x.rstrip() for x in each_line_list])

# Function to create a patient entry
def create(i):          # create patient entry
    patient_data = matrix[i]
    patient_data = [x.replace("create ", "") for x in patient_data if x.startswith("create ")]      

    # Append patient data to patient_data_list
    patient_data_list.append([patient_data[0]] + [100 * float(matrix[i][1])] + matrix[i][2:-1] + [int(100 * float(matrix[i][5]))]) 
    patient_names.append(patient_data[0])
    FileOperations.writeFile(f"Patient {patient_data[0]} is recorded.\n")

    # Calculate probability if data is incomplete
    for patient in patient_data_list:
        try:
            if patient[6] is not None:
                pass
        except IndexError:
            accuracy = patient[1] / 100
            incidence = patient[3].split("/")       # incidence[0] = ill people     incidence[1] = total people
            
            nominator = accuracy * int(incidence[0] )
            denominator = (1 - accuracy) * (int(incidence[1]) - int(incidence[0]))
            probability = nominator / (denominator + nominator)
            patient.append(round(100 * probability, 2))
            
# Function to remove a patient entry
def remove(i):
    remove_data = matrix[i]
    remove_data = [x.replace("remove ", "") for x in remove_data if x.startswith("remove ")]
    remove_name = remove_data[0]
    if (remove_name in patient_names):
        patient_names.remove(remove_name)
        for k in patient_data_list:
            if k[0] == remove_name:
                patient_data_list.remove(k)
        FileOperations.writeFile(f"Patient {remove_name} is removed.\n".format(k[0].strip()))
    else:
        FileOperations.writeFile(f"Patient {remove_name} cannot be removed due to absence.\n")

# Function to list patient entries
def list():
    list_top=["Patient","\t","Diagnosis","\t","Disease","\t\t\t","Disease","\t\t","Treatment","\t\t","Treatment",
              "\nName","\t","Accuracy","\t","Name","\t\t\t","Incidence","\t","Name","\t\t\t","Risk\n"]
    
    FileOperations.writeFile(("-")*73+"\n", list_top)
    for i in range(len(patient_data_list)):
        FileOperations.writeFile(f"{patient_data_list[i][0].ljust(8)}{patient_data_list[i][1]:.2f}%\t\t{patient_data_list[i][2].ljust(16)}" +
                                 f"{patient_data_list[i][3].ljust(12)}{patient_data_list[i][4].ljust(16)}{patient_data_list[i][5]}%\n")

# Function that calculate the probability that a patient is really ill based on 
# their diagnosis accuracy and the incidence of the disease in the population.
def probability(i):
    patient_name = matrix[i][0].lstrip("probability ")
    for patient in patient_data_list:
        if patient_name in patient:
            FileOperations.writeFile(f"Patient {patient[0]} has a probability of {patient[6]}% of having {patient[2].lower()}.\n")
            return
       
    FileOperations.writeFile(f"Probability for {patient_name} cannot be calculated due to absence.\n")

# Function to make treatment recommendation for a patient
def recommendation(i):
    patient_name = matrix[i][0].lstrip("recommendation ")
    for patient in patient_data_list:
        if (patient_name in patient):
            if patient[5] < patient[6]:
                FileOperations.writeFile(f"System suggests {patient_name} to have the treatment.\n")
            else:
                FileOperations.writeFile(f"System suggests {patient_name} NOT to have the treatment.\n")
            return
        
    FileOperations.writeFile(f"Recommendation for {patient_name} cannot be calculated due to absence.\n")

# Main loop to process commands
for i in range(len(matrix)):
    if matrix[i][0].startswith("create"):       
        create(i)                            
    elif matrix[i][0][0:6]=="remove":
        remove(i)         
    elif matrix[i][0][0:4]=="list":
        list()                       
    elif matrix[i][0][0:11]=="probability":
        probability(i)                         
    elif matrix[i][0][0:14]=="recommendation":
        recommendation(i)                  
