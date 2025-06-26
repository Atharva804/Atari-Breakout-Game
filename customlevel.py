import Constants

class CustomLevel:
    def __init__(self):
        self.level_text = None

    # function which reads from already made file
    def reading(self):
        try:
            with open(Constants.LEVELFILE, "r") as fileRead:
                self.user_text = fileRead.read()
                return self.user_text
        except Exception as e:
            print("There is a problem reading the file", str(e))

    # function to insert text in txt file
    def write(self):
        try:
            
            with open(Constants.LEVELFILE, "w") as file:
                while True:
                    self.level_text = input("Enter the levels: ")
                    if not self.level_text:
                        break 
                    file.write(self.level_text + '\n')
                file.close()
                result = self.reading()
                return result
        except Exception as e:
            print("There is a problem", str(e))

    # function which sets the given input in correct format to append in levels in BreakoutGame.py
    def create_custom_level(self):
        new_level = []
        new_level_dict = {}
        custom_config = self.write()
        print(custom_config)
        if custom_config != "":
            lines = custom_config.strip().split('\n')
            for line in lines:
                string_list = line.split(',')
                int_list = [int(digit) for digit in string_list]
                new_level.append(int_list)
            new_level_dict["bricks"] = new_level
        else :
            print("Empty Level! Please enter values for setting custom level")
            self.create_custom_level()
        return new_level_dict