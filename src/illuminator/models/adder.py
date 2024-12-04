"""
An example of creating a model for the illuminator.
The model is a simple adder that adds two inputs and 
stores the result in an output.
"""
from typing import List

from illuminator.builder import IlluminatorModel, ModelConstructor


# Define the model parameters, inputs, outputs...
adder = IlluminatorModel(
    parameters={"param1": "addition"},
    inputs={"in1": 10, "in2": 20},
    outputs={"out1": 0},
    states={"out1": 0},
    time_step_size=1,
    time=None,
    model_type='Adder'
)


# construct the model
class Adder(ModelConstructor):

    def __init__(self):
        """Associates one IlluminatorModel with the ModelConstructor"""
        super().__init__(model=adder) # this is necessary to register a IlluminatorModel  its constructor
    
    def step(self, time, inputs, max_advance=900) -> None:
        print(f"inputs: {inputs}")
        print(f'internal inputs: {self._model.inputs}')
        for eid, attrs in inputs.items():
            # print(f"eid: {eid}, attrs:{attrs}")
            # print(f"self.model_entities: {self.model_entities}")
            model_instance = self.model_entities[eid]
            for inputname, value in inputs[eid].items():
                # print(f"inputname: {inputname}, value:{value}")
                # print(f"model_instance.inputs[inputname]: {model_instance.inputs[inputname]}")
                if len(value) > 1:
                    raise RuntimeError(f"Why are you passing multiple values {value}to a single input? ")
                else:
                    first_key = next(iter(value))
                    model_instance.inputs[inputname] = value[first_key]
                    # print(f"The dictionary value: {value[first_key]}")

        self._model.outputs["out1"] = self._model.inputs["in1"] + self._model.inputs["in2"] 
        print("result:", self._model.outputs["out1"])

        return time + self._model.time_step_size

    
if __name__ == '__main__':
    # Create a model by inheriting from ModelConstructor
    # and implementing the step method
    adder_model = Adder()
    print(type(adder_model))

    print(adder_model.create(1))

    # print('model: ', adder_model.model)
    # set model to constructor
    # adder_model.model = adder

    # print(adder_model.model)
    # print('type adder model:', type(adder_model))
    # print('simulator meta:', adder_model.model.simulator_meta)


    # Documentation: adder and other models in the illuminator are
    # metadata and business logic containers. Computatation are delegated
    # to the simulation engine, which in turns uses Mosaik to run and manage the simulations.   


    # print(adder_model.step(1))