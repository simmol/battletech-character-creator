import yaml


# Get base stats and values
def get_base_attributes():
    with open( 'data/base_stats.yaml', 'r' ) as ff:
        attributes = yaml.load( ff )

    return attributes


# Get Affiliations data
def get_affiliations():
    with open( 'data/affiliations.yaml', 'r' ) as f:
        affiliations_data = yaml.load( f )

    return affiliations_data


# Get Early Childhood
def get_early_childhoods():
    with open( 'data/early_childhood.yaml', 'r' ) as f:
        early_childhoods = yaml.load( f )

    return early_childhoods


# Get Late Childhood data
def get_late_childhoods():
    with open( 'data/late_childhood.yaml', 'r' ) as f:
        late_childhoods = yaml.load( f )

    return late_childhoods


# Get Higher Education
def get_higher_education():
    with open( 'data/higher_education.yaml', 'r' ) as f:
        higher_educations = yaml.load( f )

    return higher_educations


# Get Master Fields list
def get_master_fields_list():
    with open( 'data/master_fields_list.yaml', 'r' ) as f:
        master_fields_list = yaml.load( f )

    return master_fields_list


# Get Real life modules
def get_real_life_modules():
    with open( 'data/real_life.yaml', 'r' ) as f:
        real_life_modules = yaml.load( f )

    return real_life_modules
