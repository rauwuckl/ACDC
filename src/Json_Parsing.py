import json as jn
import re

#Pattern to strip numbers from names
pattern_name = re.compile("([a-zA-Z]*)")

#Loads the Json using the Patient ID
def load_record(patient_id):
    try:
        #EDIT PATH TO MATCH YOUR LOCAL WORKSPACE
        path = '/Users/Paperplane/PycharmProjects/OxfordHack/fixtures/records/' + patient_id + '.json'
        return jn.load(open(path))
    except IOError:
        print('cannot open ', path)
        raise ValueError("cannot open {}".format(patient_id))

#Extracts basic data; name, date of birth, gender and returns as dictionary
def get_personal_details(patient_record):
    patient_f_name = pattern_name.search(patient_record['entry'][1]['resource']['name'][0]['family'])[0]
    patient_g_name = pattern_name.search(patient_record['entry'][1]['resource']['name'][0]['given'][0])[0]
    patient_title = pattern_name.search(patient_record['entry'][1]['resource']['name'][0]['prefix'][0])[0]
    patient_gender = patient_record['entry'][1]['resource']['gender']
    patient_dob = patient_record['entry'][1]['resource']['birthDate']

    details = {
        'title': patient_title,
        'g_name': patient_g_name,
        'f_name': patient_f_name,
        'gender': patient_gender,
        'dob': patient_dob
    }

    return details

#Extracts conditions; name, date observed, status
def get_conditions(patient_record):
    count = 0
    conditions = {}
    for entry in range(0, len(patient_record['entry'])):
        if (patient_record['entry'][entry]['resource']['resourceType'] == "Condition"):
            condition_name = patient_record['entry'][entry]['resource']['code']['text']
            condition_onset = patient_record['entry'][entry]['resource']['onsetDateTime']
            condition_status = patient_record['entry'][entry]['resource']['clinicalStatus']
            cond = {
                'cond_name': condition_name,
                'cond_onset': condition_onset,
                'cond_status': condition_status
            }
            conditions['condition'+str(count)] = cond
            count += 1
    return conditions

#Extracts observations; type, value, date. Calls function to only return most recent of type
def get_observations(patient_record):
    observations = {}
    count = 0
    for entry in range(0, len(patient_record['entry'])):
        if (patient_record['entry'][entry]['resource']['resourceType'] == "Observation"):
            ob = {}
            ob['type'] = patient_record['entry'][entry]['resource']['code']['coding'][0]['display']
            ob['date'] =  patient_record['entry'][entry]['resource']['issued']
            ob['values'] = find_obs_qty(patient_record['entry'][entry]['resource'])
            observations['obsv'+str(count)] = ob
            count += 1
    return most_recent_observations(observations)

#Extracts observation values; type, value, unit
def find_obs_qty(path,):
    val = {}
    for value in path:
        if value == "valueQuantity":
            val['value'] = path['valueQuantity']['value']
            val['unit']  = path['valueQuantity']['unit']
        elif value == "component":
            count = 0
            val = {}
            for com in path['component']:
                sub_val = {}
                sub_val['subtype'+str(count)] = path['component'][count]['code']['coding'][0]['display']
                sub_val['value'] = path['component'][count]['valueQuantity']['value']
                sub_val['unit'] = path['component'][count]['valueQuantity']['unit']
                count += 1
                val['val'+str(count)]=sub_val
    return val

#Extracts medication; TODO
def get_medication(patient_record):
    return None

#Selects most recent observations of a type
def most_recent_observations(obs):
    recorded = []
    most_recent = {}
    for ob in obs:
        most_recent[obs[ob]['type']] = obs[ob]
    return most_recent

#CALL THIS FUNCTION
def build_file(patient_id):
    patient_record = load_record(patient_id)
    patient_details = get_personal_details(patient_record)
    patient_conditions = get_conditions(patient_record)
    patient_observations = get_observations(patient_record)
    patient_file = {
        'details': patient_details,
        'conditions': patient_conditions,
        'observations': patient_observations
    }
    return patient_file # easier use in flask



