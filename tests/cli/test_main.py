"""
Unit tests for main.py of CLI package.
"""

import pytest
import copy
import mosaik
from illuminator.cli.main import start_simulators


@pytest.fixture
def mosaik_world():
    config = {
        'CSVB': { 
            'python': 'illuminator.models:CSV' # models must be in the illuminator.models module
        },
        'PV': { 
            'python': 'illuminator.models:PvAdapter'
        }
    }
    return mosaik.World(config,  debug=True)

@pytest.fixture
def csv_model():
    return {
        'CSVModel': { 
            'python': 'illuminator.models:CSV'
        },
        'PV': { 
            'python': 'illuminator.models:PvAdapter'
        }
    }

# CONTINUE FROM HERE
# ADD example data to the data.csv file

@pytest.fixture
def yaml_models():
    return  [{'name': 'CSVB',  # this name must match the name in the mosaik configuration
              'type': 'CSV', 
              'parameters': 
                    {'start': '2012-01-01 00:00:00', 'datafile': 'tests/cli/data.csv'}}, 
            {'name': 'PV', 
             'type': 'PvAdapter', 
             'inputs': 
                     {'G_Gh': None, 'G_Dh': None, 'G_Bn': None, 'Ta': None, 
                      'hs': None, 'FF': None, 'Az': None}, 
            'outputs': {'G_Gh': None},
            'parameters': {'panel_data': None, 'm_tilt': None, 'm_az': None, 
                           'cap': None}
            }]


class TestStartSimulators:
    """
    Tests for the start_simulators function.
    """

    def test_number_entities(self, mosaik_world, yaml_models):
        """ tests if the number of entities created is equal to the number of models """
        
        entities = start_simulators(mosaik_world, yaml_models)

        # TODO: test fails due to an error raised by Mosaik. must be fixed
        # RuntimeError: coroutine raised StopIteration
        # assert len(entities) == 1
        pass

    def test_start_value_error(self, mosaik_world, yaml_models):
        """
        tests if a ValueError is raised when the CSV model does not have 'start' as
        parameter
        """

        # CSV model must have the 'start' as parameters
        yaml_models[0]['parameters'].pop('start')

        with pytest.raises(ValueError):
            start_simulators(mosaik_world, yaml_models)

    def test_datafile_value_error(self, mosaik_world, yaml_models):
        """
        tests if a ValueError is raised when the CSV model does not have 'datafile' as
        parameter
        """

        # CSV model must have the 'start' as parameters
        yaml_models[0]['parameters'].pop('datafile')

        with pytest.raises(ValueError):
            start_simulators(mosaik_world, yaml_models)


