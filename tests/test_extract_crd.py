import os
import tempfile
import unittest
import textwrap
from pathlib import Path
import yaml

from src.extract_crd import extract_crds_from_rendered_yaml

class TestExtractCRDs(unittest.TestCase):
    def setUp(self):
        self.rendered_yaml = """\
---
apiVersion: v1
kind: Service
metadata:
  name: my-service
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crd1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crd2
"""

    def test_extract_and_concatenate_crds(self):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary rendered YAML file
            temp_file = os.path.join(temp_dir, 'rendered.yaml')
            with open(temp_file, 'w') as file:
                file.write(self.rendered_yaml)

            # Create the output directory
            output_dir = os.path.join(temp_dir, 'output')
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Call the function to extract and concatenate CRDs
            extract_crds_from_rendered_yaml(temp_file, output_dir)

            # Verify the concatenated CRDs file
            concatenated_file = os.path.join(output_dir, 'crdsOnly.yaml')
            self.assertTrue(os.path.isfile(concatenated_file))

            # Load the concatenated CRDs YAML
            with open(concatenated_file, 'r') as file:
                concatenated_yaml = file.read()

            # Verify the contents of the concatenated CRDs YAML
            expected_yaml = """\
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crd1

---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crd2

---
"""
            print('# EXPECTED YAML:')
            print(expected_yaml, '  ')
            print('# ACTUAL YAML:')
            print(concatenated_yaml, '  ')

            self.assertEqual(concatenated_yaml, expected_yaml)

if __name__ == '__main__':
    unittest.main()
