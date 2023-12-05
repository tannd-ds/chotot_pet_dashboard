import pickle
import numpy as np


class Models():
    def __init__(self, pickles_path: str = './pickles/'):
        with open(pickles_path + 'model_linear', 'rb') as file:
            self.linear_reg_model = pickle.load(file)
        with open(pickles_path + 'model_lasso', 'rb') as file:
            self.lasso_reg_model = pickle.load(file)
        with open(pickles_path + 'model_ridge', 'rb') as file:
            self.ridge_reg_model = pickle.load(file)
        with open(pickles_path + 'model_forest', 'rb') as file:
            self.random_forest_model = pickle.load(file)
        with open(pickles_path + 'model_decision', 'rb') as file:
            self.decision_tree_model = pickle.load(file)

        # Load Encoder
        with open(pickles_path + 'pet_breed_name_encoder', 'rb') as file:
            self.breed_name = pickle.load(file)
        with open(pickles_path + 'pet_age_name_encoder', 'rb') as file:
            self.age_name = pickle.load(file)
        with open(pickles_path + 'pet_size_name_encoder', 'rb') as file:
            self.size_name = pickle.load(file)
        with open(pickles_path + 'pet_type_name_encoder', 'rb') as file:
            self.type_name = pickle.load(file)
        with open(pickles_path + 'pet_breed_encoder', 'rb') as file:
            self.breed = pickle.load(file)
        with open(pickles_path + 'area_name_encoder', 'rb') as file:
            self.area_name = pickle.load(file)
        with open(pickles_path + 'ward_name_encoder', 'rb') as file:
            self.ward_name = pickle.load(file)
        with open(pickles_path + 'region_name_encoder', 'rb') as file:
            self.region_name = pickle.load(file)

        # Load OneHotEncoder
        with open(pickles_path + 'one_hot_encoder', 'rb') as file:
            self.ct = pickle.load(file)

        print('Successfully initializing models.')

    def handle_pet_breed(self, value):
        if (value < 1.0) or (value > 33.0):
            return False
        return True

    def handle_pet_breed_name(self, value):
        if value not in self.breed_name.classes_:
            return 'Khác'
        return value

    def handle_pet_age_name(self, value):
        if value not in self.age_name.classes_:
            return 'Khác (không xác định được)'
        return value

    def handle_pet_size_name(self, value):
        if value not in self.size_name.classes_:
            return 'Khác (không xác định được)'
        return value

    def handle_pet_type_name(self, value):
        if value not in self.type_name.classes_:
            return 'Thú cưng khác'
        return value

    def handle_area_name(self, value):
        # Handle Syntax
        l = ['Huyện ', 'Quận ', 'Thị xã ', 'Thành phố ']
        flag_1 = False
        for each in l:
            if each in value:
                flag_1 = True
        if flag_1 is False:
            print(f'{value} không hợp lệ')

        # Handle Exist Value
        flag_2 = True
        if value not in self.area_name.classes_:
            flag_2 = False
            print(f'{value} không tồn tại trong list các thành phố')
        return (flag_1 is True) & (flag_2 is True)

    def handle_ward_name(self, value):
        # Handle Syntax
        l = ['Xã ', 'Thị trấn ', 'Phường ']
        flag_1 = False
        for each in l:
            if each in value:
                flag_1 = True
        if flag_1 is False:
            print(f'{value} không hợp lệ')

        # Handle Exist Value
        flag_2 = True
        if value not in self.ward_name.classes_:
            flag_2 = False
            print(f'{value} không tồn tại trong list các phường xã')
        return (flag_1 is True) & (flag_2 is True)

    def handle_region_name(self, value):
        if value not in self.region_name.classes_:
            print(f'{value} không tồn tại trong list các tỉnh thành')
            return False
        return True

    def check_input(self, input):
        if self.handle_pet_breed(input['pet_breed']) is False:
            print('Pet breed phải nằm trong khoảng từ 1 đến 33')
            return False

        if self.handle_area_name(input['area_name']) is False:
            return False

        if self.handle_ward_name(input['ward_name']) is False:
            return False

        if self.handle_region_name(input['region_name']) is False:
            return False

        input['pet_breed_name'] = self.handle_pet_breed_name(
            input['pet_breed_name']
        )
        input['pet_age_name'] = self.handle_pet_age_name(
            input['pet_age_name']
        )
        input['pet_size_name'] = self.handle_pet_size_name(
            input['pet_size_name']
        )
        input['pet_type_name'] = self.handle_pet_type_name(
            input['pet_type_name']
        )

        return True

    def predict(self, dic, beautiful_display: bool = False):
        self.check_input(dic)
        pet_breed = self.breed.transform(
            np.reshape(dic['pet_breed'], -1)
        )
        pet_breed_name = self.breed_name.transform(
            np.reshape(dic['pet_breed_name'], -1)
        )
        pet_age_name = self.age_name.transform(
            np.reshape(dic['pet_age_name'], -1)
        )
        pet_size_name = self.size_name.transform(
            np.reshape(dic['pet_size_name'], -1)
        )
        pet_type_name = self.type_name.transform(
            np.reshape(dic['pet_type_name'], -1)
        )

        longtitude = dic['longtitude']
        latitude = dic['latitude']

        area = self.area_name.transform(
            np.reshape(dic['area_name'], -1)
        )
        ward = self.ward_name.transform(
            np.reshape(dic['ward_name'], -1)
        )
        region = self.region_name.transform(
            np.reshape(dic['region_name'], -1)
        )

        pet_input = np.array([
            longtitude,
            latitude,
            pet_type_name[0],
            pet_breed_name[0],
            pet_age_name[0],
            pet_size_name[0],
            pet_breed[0],
            area[0],
            ward[0],
            region[0]
        ]).reshape(1, -1).astype(object)
        pet_input = self.ct.transform(pet_input)

        output_linear = self.linear_reg_model.predict(pet_input).item()
        output_lasso = self.lasso_reg_model.predict(pet_input).item()
        output_ridge = self.ridge_reg_model.predict(pet_input).item()
        output_forest = self.random_forest_model.predict(pet_input).item()
        output_decision = self.decision_tree_model.predict(pet_input).item()

        output = {
            'linear': output_linear * 1e6,
            'lasso': output_lasso * 1e6,
            'ridge': output_ridge * 1e6,
            'random_forest': output_forest * 1e6,
            'decision_tree':  output_decision * 1e6,
        }

        if beautiful_display is True:
            for k, o in output.items():
                price_tags = ['', 'K', 'M', 'B']
                n_divided = 0

                while o > 1000:
                    o /= 1_000
                    n_divided += 1

                o = f"{o:.2f}{price_tags[n_divided]}"
                output[k] = o
            return output
        return {k: f'{v:.0f}' for (k, v) in output.items()}
