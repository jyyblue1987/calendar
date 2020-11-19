class Gregorian_Calendar:
    
    def __init__(self):
        self.month_dict = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31,
                           "Jun": 30,"Jul": 31, "Aug": 31, "Sep": 30, "Oct": 31,
                           "Nov": 30, "Dec": 31}
        self.month_dict_leap = {"Jan": 31, "Feb": 29, "Mar": 31, "Apr": 30, "May": 31,
                                "Jun": 30, "Jul": 31, "Aug": 31, "Sep": 30, "Oct": 31,
                                "Nov": 30, "Dec": 31}
        
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
      
        if is_leap_year(year):
            month_dict = self.month_dict_leap
        else:
            month_dict= self.month_dict
            
        total_days_of_month = month_dict[month]
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
        if is_leap_year(year):
            total_days_of_year = 366
            
        if day_of_year < 1:
            raise ValueError('Day of Year cannot be less than 1')
            
        
        if day_of_year > total_days_of_year:
            raise ValueError('Day of Year cannot be bigger than ' +
                             str(total_days_of_year) + ' of ' + str(year))
        return True
    
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
        
        
    def day_of_year_to_date(self, day_of_year, year):
        day_of_year = int(day_of_year)
        total_days = 0   
        
        self.is_valid_day_of_year(year, day_of_year)

        if is_leap_year(year):
            month_dict = self.month_dict_leap
        else:
            month_dict= self.month_dict

        for k,v in month_dict.items():
            if total_days < day_of_year and day_of_year <= total_days + int(v):
                sub = day_of_year - total_days
               
                return k, sub, year

            total_days += int(v)
            
        return "", 0, 0
            
    def day_of_the_year(self, month, day, year):
        self.is_valid_day(year, month, day)
        
        d = int(day)
        month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                      "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        m = month_dict[month]
        if is_leap_year(year):
            a = 1
        else:
            a = 2
        b = int((275 * m) / 9) - a * int((m + 9) / 12) + d - 30
        
        return b, year
    
    def date_to_day_of_week(self, month, day, year):
        self.is_valid_day(year, month, day)                                       
        month_dict = {"Jan": 13, "Feb": 14, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                      "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        day_dict = {"Saturday": 0, "Sunday": 1, "Monday": 2, "Tuesday": 3,
                    "Wednesday": 4, "Thursday": 5, "Friday": 6}
        m = month_dict[month]
        d = int(day)
        y = int(year)
        if m >= 13:
            y = y - 1
            
        day_of_week = (d + (13 * (m + 1) // 5) + y + (y // 4) - (y // 100) +
                       (y // 400)) % 7
        
        for day, number in day_dict.items():
            if number == day_of_week:
                return day
            
    def day_of_year_to_day_of_week(self, year, day_of_year):
        self.is_valid_day_of_year(year, day_of_year)
        month, day, year = self.day_of_year_to_date(day_of_year, year) 
        return self.date_to_day_of_week(month, day, year)
