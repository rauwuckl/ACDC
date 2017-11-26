import datetime
import src.Json_Parsing as Json_Parsing
import src.get_papers as get_papers

def get_patient_data(patient_id):
    patient_data = Json_Parsing.build_file(patient_id)

    personal_details = patient_data['details']
    personal_details['age'] = calculate_age(personal_details['dob'])

    conditions = list(patient_data['conditions'].values())

    observations = clean_observations(patient_data['observations'])

    relevant_paper_raw = get_papers.get_relevant_papers(patient_id)

    relevant_paper = clean_relevant_paper(relevant_paper_raw)

    return dict(paper=relevant_paper, personal_details=personal_details, patient_id=patient_id, conditions=conditions, observations=observations)

def clean_observations(observations_dict):
    obs_list = list(observations_dict.values())

    for obs in obs_list:
        values = obs['values']
        val, unit = get_unique_value_string(values)
        obs['val'] = val
        obs['unit'] = unit
    return obs_list

def clean_relevant_paper(raw_paper):
    collector = list()
    for paper in raw_paper.values():
        clean_paper = dict()
        clean_paper['title'] = paper['dc:title']
        clean_paper['author'] = paper['dc:creator']
        clean_paper['date'] = paper['prism:coverDate']

        pii_value = paper.get("pii", None)
        if pii_value:
            clean_paper['url'] = "https://www.sciencedirect.com/science/article/pii/{}".format(pii_value)
        else:
            clean_paper['url'] = None

        # TODO add paper url
        collector.append(clean_paper)
    return collector


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