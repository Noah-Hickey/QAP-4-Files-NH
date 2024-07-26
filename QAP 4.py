# Description: Python QAP 4 - One Stop Insurance Company
# Author: Noah Hickey
# Date(s): July 16th, 2024 - July 26th, 2024

#Import Necessary libraries
import datetime
import time
import FormatValues as FV
import sys

#Constants
CurrDate = datetime.datetime.now()


#Lists
ProvLst = [ "NL", "NS", "PE", "NB", "QC", "ON" ]
ValidPayLst= ["Full", "Monthly", "Down Pay"]

#Function to calculate monthly payments
def CalcMonthPayments(TotCost, DownPay, PROCFEE):
    RemainBalance = TotCost - DownPay
    MonthlyPayment = (RemainBalance + PROCFEE) / 8
    return RemainBalance, MonthlyPayment

def ProgressBar(iteration, total, prefix='', suffix='Complete', length=50):
    fill = '█'
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()


print()
print("             One Stop Insurance Company")
print("===================================================")
print()

#Open Constants data file
f = open("Const.dat", "r")

POLNUM = int(f.readline().strip())
BASICPREM = float(f.readline().strip())
DISCOUNTRATE = float(f.readline().strip())
LICOVAMT = float(f.readline().strip())
GLASSCOVAMT = float(f.readline().strip())
LOANCOVAMT = float(f.readline().strip())
HSTRATE = float(f.readline().strip())
PROCFEE = float(f.readline().strip())

f.close()

while True:
    #Gather user input
    CustFirName = input("Enter customer's first name: ").title()

    CustLastName = input("Enter customer's last name: ").title()

    CustName = CustFirName + " " + CustLastName
    
    StAddress = input("Enter customer's street address: ").title()
    CityAddress = input("Enter customer's city: ").title()

    while True:
        Prov = input("Enter the province (XX) - Valid Provinces are NL, NS, PE, NB, QC, & ON: ").upper()
        if Prov == "":
                print("Error - Province cannot be blank - Please try again.")
        elif len(Prov) != 2:
                print("Error - Province is a 2 digit code - Please try again.")
        elif Prov not in ProvLst:
                print("Error - Not a valid province - please reenter.")
        else:
            break

    time.sleep(2)
    print("Province has been successfully entered and is valid.")
    time.sleep(1)
    
    PostCode = input("Enter the postal code (X#X#X#): ").upper()
    if PostCode == "":
            print("Data Entry Error - Province cannot be blank - Please try again.")
    elif len(PostCode) != 6:
            print("Data Entry Error - Postal Code must be 6 characters - Please try again.")


    NumCars = int(input("Enter the number of cars being insured: "))
    

    LiCov = input("Enter if customer wants extra liability up to $1,000,000 (Y/N): ").upper()
    if LiCov == "Y":
        LiCov = LICOVAMT
    else:
        LiCov = 0

    GlassCov = input("Enter if customer wants optional glass coverage (Y/N): ").upper()
    if GlassCov == "Y":
        GlassCov = GLASSCOVAMT
    else:
        GlassCov = 0

    LoanCar = input("Enter if customer wants an optional loaner car (Y/N): ").upper()
    if LoanCar == "Y":
        LoanCar = LOANCOVAMT
    else:
        LoanCar = 0

    while True:
        PayType = input("Enter payment schedule: Full, Monthly, or Down Payment (Full/Monthly/Down Pay): ").title()
        if PayType in ValidPayLst:
            if PayType == "Down Pay":
                while True:
                    try:
                        DownPayment = float(input("Enter down payment amount: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number for the down payment.")
            else:
                DownPayment = 0  
            break  
        else:
            print("Data Entry Error - Not a valid payment method. Please enter Full, Monthly, or Down Pay.")


    ClaimNum = int(input("Enter claim number: "))

    ClaimDate = input("Enter the claim date (YYYY-MM-DD): ")
    ClaimDate = datetime.datetime.strptime(ClaimDate, "%Y-%m-%d")
    Formatted_ClaimDate = ClaimDate.strftime("%Y-%m-%d")

    ClaimAmt = float(input("Enter the claim amount:"))


    #Calculate premium cost
    TotPremium = BASICPREM
    if NumCars > 1:
        TotPremium += (NumCars - 1) * BASICPREM * (1 - DISCOUNTRATE)

    #Calculate Coverages
    TotExtraCosts = 0
    if LiCov == "Y":
        TotExtraCosts += LICOVAMT * NumCars
    if GlassCov == "Y":
        TotExtraCosts += GLASSCOVAMT * NumCars
    if LoanCar == "Y":
        TotExtraCosts += LOANCOVAMT * NumCars

    TotPremium += TotExtraCosts

    # Calculate HST and total cost
    HST = TotPremium * HSTRATE
    TotCost = TotPremium + HST

    # Calculate remaining balance and monthly payment if applicable
    if PayType == "Monthly":
        RemainBalance, MonthlyPayment = CalcMonthPayments(TotCost, 0, PROCFEE)
    elif PayType == "Down Pay":
        RemainBalance, MonthlyPayment = CalcMonthPayments(TotCost, DownPayment, PROCFEE)
    else:
        MonthlyPayment = 0
        RemainBalance = TotCost  # Assuming full payment, remaining balance is the total cost
    
    #Calculate next payment date from function
    InvoiceDate = datetime.date.today()
    if InvoiceDate.month == 12:
        FirstPaymentDate = InvoiceDate.replace(year=InvoiceDate.year + 1, month=1, day=1)
    else:
        FirstPaymentDate = InvoiceDate.replace(month=InvoiceDate.month + 1, day=1)

   
    # Progress bar before printing receipt
    total_steps = 10
    for step in range(1, total_steps + 1):
        ProgressBar(step, total_steps, prefix='Processing:', suffix='Complete', length=50)
        time.sleep(0.1)  # Simulate processing time

    #Print formatted receipt
    print()
    print("                          One Stop Insurance Company                                   ")
    print("=======================================================================================")
    print()
    print(f"INS. POLICY #: {POLNUM:<4d}                             INVOICE DATE: {InvoiceDate}")                                
    print()
    print("________________________________________________________________________________________")
    print("CUSTOMER NAME                PROV.          ADDRESS                  POSTAL CODE    ")
    print()
    print("=======================================================================================")
    print()
    print(f"{CustName:<13s}                  {Prov:<2s}          {CityAddress:<13s}                {PostCode:<6s}")
    print()
    print("________________________________________________________________________________________")
    print("# OF VEHICLES         EXTRA LIABILITY        GLASS COVERAGE       LOANER CAR")
    print()
    print("=======================================================================================")
    print()
    print(f"{NumCars}                           {FV.FDollar2(LiCov)}              {FV.FDollar2(GlassCov)}             {FV.FDollar2(LoanCar)}")
    print("________________________________________________________________________________________")
    print("CLAIM #              CLAIM DATE    ")
    print()
    print("=======================================================================================")
    print()
    print(f"{ClaimNum:>4d}                  {Formatted_ClaimDate}")
    print("________________________________________________________________________________________")
    print("TOTAL PREMIUM            TOTAL EXTRA COSTS                HST             TOTAL COST")
    print()
    print("=======================================================================================")
    print()
    print(f"{FV.FDollar2(TotPremium)}                   {FV.FDollar2(TotExtraCosts)}                        {FV.FDollar2(HST)}           {FV.FDollar2(TotCost)}")
    print("________________________________________________________________________________________")
    print()
    print()
    print("PROCESSING FEE          REMAINING BALANCE        MONTHLY PAYMENT")
    print()
    print("=======================================================================================")
    print(f"{FV.FDollar2(PROCFEE)}                          {FV.FDollar2(RemainBalance)}            {FV.FDollar2(MonthlyPayment)}")
    print("________________________________________________________________________________________")
    print()
    print(f"First Pay Date: {FirstPaymentDate}")
    print()
    print("                 Have a nice day! Thank you for choosing us!")


    #Write to data file
    with open("InsFiles.dat", "a") as f:
        f.write(f"{ClaimNum}, ")
        f.write(f"{CurrDate}, ")   
        f.write(f"{POLNUM}, ")
        f.write(f"{CustName}, ")
        f.write(f"{StAddress}, ")
        f.write(f"{CityAddress}, ")
        f.write(f"{Prov}, ")
        f.write(f"{PostCode}, ")
        f.write(f"{TotCost}, ")
        f.write(f"{NumCars}, ")
        f.write(f"{LiCov}, ")
        f.write(f"{GlassCov}, ")
        f.write(f"{LoanCar}, ")
        f.write(f"{PayType}, ")
        if PayType == "Down Payment":
            f.write(f"{DownPayment}, ")
        f.write(f"{Formatted_ClaimDate}, ")
        f.write(f"{ClaimAmt}\n")

  
    time.sleep(1)
    print()
    print("Insurance information has been successfully saved to InsFiles.dat ...")
    print()
    time.sleep(1)
    print()
    
    try:
        print("\nClaim #   Claim Date         Amount")
        print("-----------------------------------")
        with open("InsFiles.dat", "r") as f:
            for CustRecord in f:
                CustRecord = CustRecord.strip()
                if not CustRecord:
                    continue  # Skip empty lines
                CustFields = CustRecord.split(", ")
                if len(CustFields) >= 3:  # Ensure there are enough fields
                    ClaimNum = CustFields[0]
                    ClaimDate = CustFields[-2]
                    ClaimAmt = CustFields[-1]
                    print(f"{ClaimNum}   {ClaimDate}    {ClaimAmt}")
                else:
                    print("Error: Missing fields in record.")
    except FileNotFoundError:
        print("The file InsFiles.dat does not exist.")
    except Exception as e:
        print(f"An error occurred while reading from the file: {e}")

        
    #Add 1 to policy number

    POLNUM += 1

    f.close()

    print()
    Continue = input("Do you want to enter another insurance claim (Y/N): ").upper()
    if Continue == "N":
        break
    