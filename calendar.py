import re
import copy

class Calendar:
    def __init__(self):
        self.month_dict = {}
        self.day_dict = {}

    def parse_date(self, date_string):
        '''
        Extract the month, day, and year from a date string.  Acceptable formats are
          'Jour de la Révolution, 1792'  =>  month = 'Jour de la Révolution', day = None, year = 1792'
          '3/1/2020'                     =>  month = 3, day = 1, year = 2020
          '2 Lithe, 1418'                =>  month = '2 Lithe', day = None, year = 1418
          '2 Lithe 1418'                 =>  month = '2 Lithe', day = None, year = 1418
          'Sep 30, 2020'                 =>  month = 'Sep', day = 30, year = 2020
        The day and year are returned as ints, while the month is a string (as in 'Mar 1, 2020') or an int
        (as in 3/1/2020).
        '''
        date_string = date_string.replace(',', ' ').lstrip().rstrip()
        date_string = date_string.replace('/', ' ')
        # Unless you understand the following line you should experiment with this method until
        # you have a clear idea of what it does...
        p = re.compile(r'[ ]*(?P<month>[0-9]*[ ]*[\D ]+)[ ]*(?P<num1>[0-9]*)[ ]*(?P<num2>[0-9]*$)')
        match = p.match(date_string)
        if match:
            month = match.group('month').lstrip().rstrip()
            num1  = match.group('num1').lstrip().rstrip()
            num2  = match.group('num2').lstrip().rstrip()

            # Convert the month to an int if appropriate.
            if month.isdigit():
                month = int(month)

            if num1 and num2:  # Both day and year are present.
                day  = int(num1)
                year = int(num2)
            elif num1:         # Only one of day and year is present; we take it to be the year.
                day   = None
                year  = int(num1)
            else:
                day  = None    # Neither day or year is present (e.g., 'Midyear's Day').
                year = None

            return (month, day, year)
        else:
            # This branch indicates a malformed date string.
            raise ValueError(f'I cannot make sense of this date: {date_string}.')


    def is_leap_year(self, year):
        if (year % 4 == 0):
            if (year % 100 == 0):
                if (year % 400 ==0):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


    def date_to_day_of_year(self, date_string):
        # Return the day of the year (int) given a date.
        #
        # This can be called with strings such as
        #   obj.date_to_day_of_year("Messidor, 14, 1789")
        # and
        #   obj.date_to_day_of_year("Midyear"s Day, 1418")
        # You need to determine the form by parsing the string.
        month, day, year = self.parse_date(date_string)

        self.is_valid_day(year, month, day)

        month_dict = self.month_list(year)       

        

        total_days = 0
        for k,v in month_dict.items():
            if k == month:                
                if day == None:
                    total_days += 1
                else:
                    total_days += day
                break
            
            total_days += v
             
        return total_days, year

    

    def day_of_year_to_date(self, day_of_year, year):
        '''
        Convert day of year to date.
        '''
        day_of_year = int(day_of_year)
        total_days = 0   

        self.is_valid_day_of_year(year, day_of_year)

        month_dict = self.month_list(year)

        for k,v in month_dict.items():
            if total_days < day_of_year and day_of_year <= total_days + int(v):
                sub = day_of_year - total_days

                if v < 10:  # Special Days             
                    return k, year
                else:
                    return k, sub, year
            total_days += int(v)
            
        return "", 0, 0

    def month_list(self, year):
        month_dict = copy.deepcopy(self.month_dict)
        if self.is_leap_year(year) == True:
            if 'Overlithe' in month_dict:
                del month_dict['Overlithe']

            if 'Jour de la Révolution' in month_dict:
                del month_dict['Jour de la Révolution']
            if 'Feb' in month_dict:
                month_dict["Feb"] = 29
        return month_dict

    def day_name(self, day_of_week):
        for day, number in self.day_dict.items():
            if number == day_of_week:
                return day
        
        return ""

    def is_leap_year(self, year):
        self.year = year
        
        if (self.year % 4 == 0):
            if (self.year % 100 == 0):
                if (self.year % 400 ==0):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def is_valid_year(self, year):
        if year < 0:            
            raise ValueError(str(year) + ' Invalid Year') 
        return True
    
    def is_valid_month(self, month):
        exist = month in self.month_dict
        if exist == False:            
            raise ValueError(month + ' Invalid Month') 
        return exist
    
    def is_valid_day(self, year, month, day):
        if self.is_valid_year(year) == False:
            return False
        
        if self.is_valid_month(month) == False:
            return False
      
        month_dict= self.month_list(year)
            
        total_days_of_month = month_dict[month]
        if day == None and total_days_of_month < 10:
            return True;

        if day > 0 and total_days_of_month < 10:
            raise ValueError('Special days cannot have date value ' + day)

        if day < 1:            
            raise ValueError('Day cannot be less than 1')
        
        if day > total_days_of_month:            
            raise ValueError('Day cannot be bigger than ' + str(total_days_of_month) 
                             + ' of ' + str(month))
        return True
            
    def is_valid_day_of_year(self, year, day_of_year):
        if self.is_valid_year(year) == False:
            return False
      
        total_days_of_year = 365
        if self.is_leap_year(year):
            total_days_of_year = 366
            
        if day_of_year < 1:
            raise ValueError('Day of Year cannot be less than 1')
            
        
        if day_of_year > total_days_of_year:
            raise ValueError('Day of Year cannot be bigger than ' +
                             str(total_days_of_year) + ' of ' + str(year))
        return True
#---------------------------------------------------------------------------------------------------------------

class Gregorian_Calendar(Calendar):
    def __init__(self):
        # Days of the week: 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'
        # Months: 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        self.month_dict = {  
                "Jan":31, 
                "Feb": 28,
                "Mar": 31,
                "Apr": 30,
                "May": 31,
                "Jun": 30,
                "Jul": 31,
                "Aug": 31,
                "Sep": 30,
                "Oct": 31, 
                "Nov": 30,
                "Dec": 31,                
        }

        self.day_dict = {"Sat": 0, "Sun": 1, "Mon": 2, "Tue": 3,
                    "Wed": 4, "Thu": 5, "Fri": 6}


    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Messidor, 14, 1789")
        # and
        #   obj.date_to_weekday("Midyear"s Day, 1418")
        # You need to determine the form by parsing the string.

        month_dict = {"Jan": 13, "Feb": 14, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                      "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        

        month, day, year = self.parse_date(date_string)

        m = month_dict[month]
        d = int(day)
        y = int(year)
        if m >= 13:
            y = y - 1
            
        day_of_week = (d + (13 * (m + 1) // 5) + y + (y // 4) - (y // 100) +
                       (y // 400)) % 7
        
        return self.day_name(day_of_week)
    
#---------------------------------------------------------------------------------------------------------------

class Shire_Calendar(Calendar):
    def __init__(self):
        # Days of the week: "Sterday", "Sunday", "Monday", "Trewsday", "Hensday", "Mersday", "Highday"
        # Months and special days: "2 Yule", "Afteryule", "Solmath", "Rethe", "Astron", "Thrimidge", "Forelithe",
        # "1 Lithe", "Midyear"s Day", "Overlithe", "2 Lithe", "Afterlithe", "Wedmath", "Halimath", "Winterfilth",
        # "Blotmath", "Foreyule", "1 Yule"
        self.month_dict = {  
                "2 Yule":1, 
                "Afteryule": 30,
                "Solmath": 30,
                "Rethe": 30,
                "Astron": 30,
                "Thrimidge": 30,
                "Forelithe": 30,
                "1 Lithe": 1,
                "Midyear's Day": 1, 
                "Overlithe": 1,
                "2 Lithe": 1,
                "Afterlithe": 30,
                "Wedmath": 30,
                "Halimath": 30,
                "Winterfilth": 30,
                "Blotmath": 30,
                "Foreyule": 30,
                "1 Yule": 1,
        }
        
        self.day_dict = {
                    "Sterday": 1, 
                    "Sunday": 2, 
                    "Monday": 3, 
                    "Trewsday": 4, 
                    "Hensday": 5, 
                    "Mersday": 6, 
                    "Highday": 0
                    }


    def is_leap_year(self, year):
        if year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True;
        else:
            return False;
        
    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Midyear"s Day, 1418")
        #   obj.date_to_weekday("Solmath 19, 1418")
        # You need to determine the form by parsing the string.
        month, day, year = self.parse_date(date_string)

        if day == None:
            return month

        total_days, year = self.date_to_day_of_year(date_string)
        if total_days >= 183:
            if self.is_leap_year(year):
                total_days -= 2
            else:
                total_days -= 1

        day_of_week = total_days % 7

        return self.day_name(day_of_week)

#---------------------------------------------------------------------------------------------------------------

# Keep the non-ASCII characters in the strings and the class name.
class Calendrier_Républicain(Calendar):
    def __init__(self):
        # Days of the week: "primidi", "duodi", "tridi", "quartidi", "quintidi",
        #                   "sextidi", "septidi", "octidi", "nonidi", "décadi"
        # Months : "Vendémiaire", "Brumaire", "Frimaire", "Nivôse", "Pluviôse", "Ventôse",
        #          "Germinal", "Floréal", "Prairial", "Messidor", "Thermidor", "Fructidor",
        # Days at end of year: "Jour de la vertu", "Jour du génie", "Jour du travail",
        #            "Jour de l'opinion", "Jour des récompenses", "Jour de la Révolution" (leap-year only)
        #
        self.month_dict = {  
                "Vendémiaire":30, 
                "Brumaire": 30,
                "Frimaire": 30,
                "Nivôse": 30,
                "Pluviôse": 30,
                "Ventôse": 30,
                "Germinal": 30,
                "Floréal": 30,
                "Prairial": 30, 
                "Messidor": 30,
                "Thermidor": 30,
                "Fructidor": 30,
                "Jour de la vertu": 1,
                "Jour du génie": 1, 
                "Jour du travail": 1,
                "Jour de l'opinion": 1, 
                "Jour des récompenses": 1, 
                "Jour de la Révolution": 1
        }

        self.day_dict = {  
                "primidi":1, 
                "duodi":2, 
                "tridi":3, 
                "quartidi":4, 
                "quintidi":5,
                "sextidi":6, 
                "septidi":7, 
                "octidi":8, 
                "nonidi":9, 
                "décadi":0
        }



    def date_to_weekday(self, date_string):
        # This can be called with strings such as
        #   obj.date_to_weekday("Messidor, 14, 1789")
        #   obj.date_to_weekday("Jour des récompenses, 14, 1789")
        # You need to determine the form by parsing the string.
        month, day, year = self.parse_date(date_string)

        if day == None:
            return ""

        total_days, year = self.date_to_day_of_year(date_string)
        if total_days > 360:
            return ""
        
        day_of_week = total_days % 10

        return self.day_name(day_of_week)

#---------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Tests go here.
    cal = Calendar()
    print(cal.parse_date('Aug 15, 2020'))
    print(cal.parse_date("Midyear's Day 1418"))
    print(cal.parse_date("  Overlithe  1418 "))
    print(cal.parse_date("3/1/2020"))
    print(cal.parse_date('bob bob 1'))
    # print(cal.parse_date('bob 1 bob'))

    shire = Shire_Calendar()
    assert not shire.is_leap_year(1400)
    # assert shire.date_to_day_of_year('1 Lithe 1418') == 180
    assert shire.date_to_day_of_year("Midyear's Day 1418") == (183, 1418)
    assert shire.day_of_year_to_date(31, 2018) == ('Afteryule', 30, 2018)
    assert shire.day_of_year_to_date(182, 2018) == ('1 Lithe', 2018)
    assert shire.date_to_weekday("Midyear's Day 1418") == "Midyear's Day"
    assert shire.date_to_weekday("2 Yule 2020") == "2 Yule"
    assert shire.date_to_weekday("Solmath 1 2020") == "Trewsday"
    assert shire.date_to_weekday("Wedmath 1 2020") == "Trewsday"
    
    fr = Calendrier_Républicain()
    assert fr.is_leap_year(2020)
    assert fr.date_to_day_of_year("Messidor 14, 1789") == (284, 1789)
    assert fr.date_to_day_of_year("Jour de l'opinion, 1795") == (364, 1795)
    assert fr.date_to_weekday("Jour de la vertu 2020") == ""
    assert fr.date_to_weekday("Pluviôse 9 2020") == "nonidi"
    # assert fr.day_of_year_to_date("Jour de la Révolution", 2400) == ("Jour de la Révolution", 2400)

    print(fr.date_to_weekday("Jour des récompenses 2401"))

    greg = Gregorian_Calendar()
    assert greg.is_leap_year(2020)
    assert greg.day_of_year_to_date(1, 2018) == ('Jan', 1, 2018)
    assert greg.date_to_day_of_year("Mar 1, 2020") == (60, 2020)
    assert greg.date_to_weekday("Nov 19, 2020") == 'Thu'
    

    # print(greg.date_to_day_of_year("Mar 32, 2020"))
    # print(greg.day_of_year_to_date(368, 2020))
    # print(shire.date_to_weekday("1 Yule, 1, 1418 "))
    print(shire.date_to_weekday("1 Yule, 1418 "))
    print(shire.day_of_year_to_date(186, 2400))
