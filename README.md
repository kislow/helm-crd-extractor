# CRD Extractor

The CRD Extractor is a Python script that enables you to extract Custom Resource Definitions (CRDs) from a rendered YAML file and save them as a concatenated YAML file. It also separates non-CRD objects into another file.

# Prerequisites

- Python 3.x
- PyYAML library (`pip3 install pyyaml`)

# Usage

1. Make sure you have Python 3.x installed on your system.
2. Install the required PyYAML library by running the following command:
```sh
$ pip3 install -r requirements.txt
```
3. Run the script by executing the following command:
```sh
$ python3 main.py --file <rendered_yaml_file> --path <output_dir>`
```
### Notes

* The script uses the `PyYAML` library to load and dump YAML data. Make sure you have installed it before running the script.
* The script identifies CRDs by checking the `kind` attribute of each object. Objects with kind set to `'CustomResourceDefinition'` are considered as CRDs.
* The extracted CRDs will be saved in a single file with each CRD separated by `---` delimiters.
* Non-CRD objects will be saved in a separate file with the same `---` delimiters.
* The script will display the paths of the generated files after completion.

# Run Test

```sh
$ python3 -m unittest tests.test_extract_crd`
```

# License

This project is licensed under the MIT License.

Feel free to modify and use this script according to your needs.
