import os
import yaml

def extract_crds_from_rendered_yaml(yaml_file, output_dir) -> None:
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load_all(file)

        crds = []
        for obj in yaml_data:
            if obj.get('kind') == 'CustomResourceDefinition':
                crds.append(obj)

    concatenated_crd_yaml = ""
    for crd in crds:
        crd_yaml = yaml.dump(crd)
        concatenated_crd_yaml += crd_yaml + '\n---\n'

    output_file = os.path.join(output_dir, 'crdsOnly.yaml')
    with open(output_file, 'w') as output:
        output.write(concatenated_crd_yaml)
    print(f"Concatenated CRDs: {output_file}")
