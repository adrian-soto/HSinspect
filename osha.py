from numpy import isnan

def fopi(df, key):
    '''
    Fraction Of Positive Instances in DataFrame for a given key.
    This function is meant to work with (0,1) data. Unexpected
    behavior may occur when it is not.
    
    INPUT
      - df  : pandas.DataFrame
      - key : key of feature of interest
      
    OUTPUT
      - fraction of positive instances
    '''
    
    return float(sum(df[df[key]==1][key].values))/ df.shape[0]


def sic_division(sic_code):
    '''
    Given a 4-digit SIC code, return division abbreviation
    
    INPUT:
      - sic_code : 4-digit integer or real
      
    OUTPUT:
      - division : SIC code division (values A-K)
    '''
    
    # First, ensure sic_code is integer
    if (not isinstance( sic_code, int )):
        
        if (sic_code is None):
            # If data is missing, return 0
            division = "0"
            return division
        elif (isnan(sic_code) ):
            # If data is NaN, return 0
            division = "0"
            return division
        else:
            # If not missing, convert to int
            sic_code=int(sic_code)
        
    if (sic_code<100 or sic_code>9999):
        print "Warning: SIC code value ", sic_code, " is outside range (0100-9999)"
        division = "0"
    if (sic_code>=100 and sic_code<=999):
        # Agriculture, Forestry and Fishing
        division = "A"
    elif (sic_code>=1000 and sic_code<=1499):
        # Mining
        division = "B" 
    elif (sic_code>=1500 and sic_code<=1799):
        # Construction
        division = "C"
    elif (sic_code>=1800 and sic_code<=1999):
        print "Error: SIC code value ", sic_code, " is in excluded range (1800-1999)"
        quit()
    elif (sic_code>=2000 and sic_code<=3999):
        # Manufacturing
        division = "D"
    elif (sic_code>=4000 and sic_code<=4999):
        # Transportation, Communications, Electric, 
        # Gas and Sanitary service
        division = "E"
    elif (sic_code>=5000 and sic_code<=5199):
        # Wholesale trade
        division = "F"
    elif (sic_code>=5200 and sic_code<=5999):
        # Retail trade
        division = "G"
    elif (sic_code>=6000 and sic_code<=6799):
        # Finance, Insurance and Real Estate
        division = "H"
    elif (sic_code>=7000 and sic_code<=8999):
        # Services
        division = "I"
    elif (sic_code>=9000 and sic_code<=9099):
        # undetermined
        print "Warning: SIC code value ", sic_code ," is in excluded range (9000-9099)"
        division = "0"
    elif (sic_code>=9100 and sic_code<=9729):
        # Public Administration
        division = "J"
    elif (sic_code>=9730 and sic_code<=9899):
        # undetermined
        print "Warning: SIC code value ", sic_code ," is in excluded range (9730-9900)"
        division = "0"
    elif (sic_code>=9900 and sic_code<=9999):
        # Nonclassifiable
        division = "K"
    
    return division




