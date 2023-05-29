from argparse import ArgumentParser
from src.extract_crd import extract_crds_from_rendered_yaml

def parse_args():
    parser = ArgumentParser(description='extract crds from helm.yaml')
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--path', type=str, required=True)
    return parser.parse_args()

if __name__ == '__main__':
    CONFIG = parse_args()
    extract_crds_from_rendered_yaml(CONFIG.file, CONFIG.path)
