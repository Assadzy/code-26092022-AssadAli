class BMICalculator:
    """Class to Calculate the BMI (Body Mass Index) using Formula 1, BMI Category and Health risk
    Formula 1 - BMI(kg/m^2) = mass(kg) / height(m)^2
    """

    def __init__(self, _data, bmi_table):
        self.my_data = _data
        self.bmi_table = bmi_table

    def my_bmi(self, add_bmi_value=False):
        """
        :param bmi_value: If bmi value is needed in return set to True, default False
        :return: Calculate the BMI (Body Mass Index) using Formula, BMI Category and Health risk
                from Table of the person and add them as 3 new columns
        """
        table_elements = self.table_to_dict(self.bmi_table)

        final_my_data = []
        for m_h in self.my_data:
            val = m_h
            mass = val['WeightKg']
            height = val['HeightCm'] / 100
            bmi_value = mass / (height * height)
            for element in table_elements:
                given_range = element['BMI_Range']
                if '-' in given_range:
                    the_range = given_range.split(' - ')
                    if float(the_range[0]) < bmi_value < float(the_range[1]):
                        val.update(element)
                        if add_bmi_value:
                            val['bmi'] = bmi_value
                        final_my_data.append(val)
                        break

                elif (bmi_value < float(given_range.split()[0])) and ('and below' in given_range):
                    val.update(element)
                    if add_bmi_value:
                        val['bmi'] = bmi_value
                    final_my_data.append(val)
                    break

                elif (bmi_value > float(given_range.split()[0])) and ('and above' in given_range):
                    val.update(element)
                    if add_bmi_value:
                        val['bmi'] = bmi_value
                    final_my_data.append(val)
                    break
                    
        return final_my_data

    def all_stats(self):
        """
        :return: Stats of each BMI Cateogry count
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


_data = [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96},
         {"Gender": "Male", "HeightCm": 161, "WeightKg": 85},
         {"Gender": "Male", "HeightCm": 180, "WeightKg": 77},
         {"Gender": "Female", "HeightCm": 166, "WeightKg": 62},
         {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
         {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]

_table = '''BMI_Category,BMI_Range,Health_risk
Underweight, 18.4 and below, Malnutrition risk
Normal weight, 18.5 - 24.9, Low risk
Overweight, 25 - 29.9, Enhanced risk
Moderately obese, 30 - 34.9, Medium risk
Severely obese, 35 - 39.9, High risk
Very severely obese, 40 and above, Very high risk'''

if __name__ == '__main__':
    my_calculator = BMICalculator(_data, _table)
    print('--------\nCalculate the BMI (Body Mass Index) using Formula 1\n\n', my_calculator.my_bmi())
    print('--------\nAll Status for each BMI Category\n\n', my_calculator.all_stats())
    print('--------\nCount of all the overweights with BMI > 25 : ', my_calculator.count_overweight)
 