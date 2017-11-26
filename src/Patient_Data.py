import datetime
import src.Json_Parsing as Json_Parsing

def get_patient_data(patient_id):
    patient_data = Json_Parsing.build_file(patient_id)

    personal_details = patient_data['details']
    personal_details['age'] = calculate_age(personal_details['dob'])

    conditions = list(patient_data['conditions'].values())

    observations = clean_observations(patient_data['observations'])


    return dict(personal_details=personal_details, patient_id=patient_id, conditions=conditions, observations=observations)

def clean_observations(observations_dict):
    obs_list = list(observations_dict.values())

    for obs in obs_list:
        values = obs['values']
        val, unit = get_unique_value_string(values)
        obs['val'] = val
        obs['unit'] = unit
    return obs_list



def get_unique_value_string(value_dict):
    """

    :param value_dict:
    :return: (value_string, unit_string)
    """
    if 'value' in value_dict.keys():
        # there is directly a value
        return str(value_dict['value']), value_dict['unit']
    else:
        # there are multiple values
        current_unit = None
        value_collector = list()
        for single_value in value_dict.values():
            if current_unit is None:
                current_unit = single_value['unit']
            elif current_unit != single_value['unit']:
                raise ValueError("There were muliple values with different units {}".format(value_dict))
            else:
                value_collector.append(str(single_value['value']))

        return ", ".join(value_collector), current_unit





def calculate_age(birthdate_string):
    return (datetime.datetime.now() - datetime.datetime.strptime(birthdate_string, "%Y-%m-%d"))// datetime.timedelta(days=365.2425)