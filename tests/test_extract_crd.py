import os
import tempfile
import unittest
import textwrap
from pathlib import Path
import yaml

from src.extract_crd import extract_crds_from_rendered_yaml

RENDERED_YAML = textwrap.dedent("""\
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
)

expected_yaml = textwrap.dedent( """\
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
)

expected_non_crd_yaml = textwrap.dedent( """\
apiVersion: v1
kind: Service
metadata:
  name: my-service

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment

---
"""
)

class TestExtractCRDs(unittest.TestCase):
    def setUp(self):
        self.rendered_yaml = RENDERED_YAML

    def test_extract_and_concatenate_crds(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            temp_rendered_yaml_file = os.path.join(temp_dir, 'rendered.yaml')
            with open(temp_rendered_yaml_file, 'w') as file:
                file.write(self.rendered_yaml)

            output_dir = os.path.join(temp_dir, 'output')
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            extract_crds_from_rendered_yaml(temp_rendered_yaml_file, output_dir)

            # Verify concatenated CRDs file
            concatenated_file = os.path.join(output_dir, 'crdsOnly.yaml')
            self.assertTrue(os.path.isfile(concatenated_file))

            with open(concatenated_file, 'r') as file:
                concatenated_yaml = file.read()

            print('# EXPECTED YAML:')
            print(expected_yaml, '  ')
            print('# ACTUAL YAML:')
            print(concatenated_yaml, '  ')

            self.assertEqual(concatenated_yaml, expected_yaml)

            # Verify non-CRD objects file
            non_crd_file = os.path.join(output_dir, 'noCrds.yaml')
            self.assertTrue(os.path.isfile(non_crd_file))

            with open(non_crd_file, 'r') as file:
                non_crd_yaml = file.read()

            # Verify the contents of the non-CRD objects YAML
            print('# EXPECTED non-CRD YAML:')
            print(expected_non_crd_yaml, '  ')
            print('# ACTUAL non-CRD YAML:')
            print(non_crd_yaml, '  ')

            self.assertEqual(non_crd_yaml, expected_non_crd_yaml)

if __name__ == '__main__':
    unittest.main()
