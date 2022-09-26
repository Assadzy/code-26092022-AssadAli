from config import BMI_TABLE_PATH, DATA_JSON, logs_file
import json
import sys

class BMICalculator:
    """Class to Calculate the BMI (Body Mass Index) using Formula 1, BMI Category and Health risk
    Formula 1 - BMI(kg/m^2) = mass(kg) / height(m)^2
    """

    def __init__(self):
        self.bmi_table = None
        self.my_data = None
        self.get_input_data()

    def get_input_data(self):
        with open(BMI_TABLE_PATH, 'r') as f:
            self.bmi_table = f.read()
        with open(DATA_JSON, 'r') as g:
            self.my_data = json.load(g)

    def my_bmi(self, add_bmi_value=False):
        """
        :param add_bmi_value: If bmi value is needed in return set to True, default False
        :return: Calculate the BMI (Body Mass Index) using Formula, BMI Category and Health risk
                from Table of the person and add them as 3 new columns
        """
        table_elements = self.table_to_dict(self.bmi_table)

        final_data = []
        for container in self.my_data:
            mass = container['WeightKg']
            height = container['HeightCm'] / 100
            bmi_value = mass / (height * height)
            for element in table_elements:
                given_range = element['BMI_Range']
                if '-' in given_range:
                    the_range = given_range.split(' - ')
                    if float(the_range[0]) < bmi_value < float(the_range[1]):
                        container.update(element)
                        if add_bmi_value:
                            container['bmi'] = bmi_value
                        final_data.append(container)
                        break

                elif (bmi_value < float(given_range.split()[0])) and ('and below' in given_range):
                    container.update(element)
                    if add_bmi_value:
                        container['bmi'] = bmi_value
                    final_data.append(container)
                    break

                elif (bmi_value > float(given_range.split()[0])) and ('and above' in given_range):
                    container.update(element)
                    if add_bmi_value:
                        container['bmi'] = bmi_value
                    final_data.append(container)
                    break
                    
        return final_data

    def all_stats(self):
        """
        :return: Complete Stats of each BMI Category
        """
        my_data = self.my_bmi()
        table_elements = self.table_to_dict(self.bmi_table)
        bmi_keys = [x['BMI_Category'] for x in table_elements]
        all_ = []
        for element in bmi_keys:
            val = {element: len([x['BMI_Category'] for x in my_data if x['BMI_Category'] == element])}
            all_.append(val)
        return all_

    @property
    def count_overweight(self):
        all_my_data = self.my_bmi(add_bmi_value=True)
        overweight = len([x for x in all_my_data if x['bmi'] > 25])
        return overweight

    @staticmethod
    def table_to_dict(my_table):
        my_table = my_table.split('\n')
        table_elements = []
        for element in my_table[1:]:
            item = dict(
                zip(my_table[0].split(','), [d.strip() if str(d).strip() != '' else None for d in element.split(',')]))
            table_elements.append(item)
        return table_elements

if __name__ == '__main__':

    # comment this to show statements in terminal, otherwise see files/app.log file
    sys.stdout = open(logs_file, "w", buffering=1, encoding='utf-8')
    my_calculator = BMICalculator()
    print('--------\nCalculate the BMI (Body Mass Index) using Formula 1\n\n', my_calculator.my_bmi())
    print('--------\nAll Stats for each BMI Category\n\n', my_calculator.all_stats())
    print('--------\nCount of all the overweights with BMI > 25 : ', my_calculator.count_overweight)

 