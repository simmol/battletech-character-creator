import yaml

with open('data/affiliations.yaml', 'r') as f:
    affiliations = yaml.load(f)

print affiliations
