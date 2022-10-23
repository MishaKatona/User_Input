from .Build_helpers.Frame_container import FrameContainer
from .Build_helpers.Definition_clusterer import ClusterDefinitions
from .Build_helpers.Templater import Templater
from .Tools import flatten
from .Frame.Frame import Frame
from .Build_helpers.Widget import Widget


class WidgetBuilder:

    def __init__(self,
                 default_template: dict,
                 template_lst: list,
                 input_element_template: dict,
                 body_dict_list: dict,
                 build_settings: dict,
                 logger):

        self.build_settings = build_settings
        self.logger = logger

        # Set up the templater
        self.templater = Templater(default_template=default_template,
                                   template_lst=template_lst,
                                   input_element_template=input_element_template,
                                   body_dict_list=body_dict_list,
                                   logger=logger)

    def build_widget(self,
                     input_definitions: dict,
                     definitions_depth: int,
                     callback,
                     parent=[]):

        # Flatten input definitions and inject Path related metadata
        definitions = flatten(nested_dict=input_definitions,
                              depth=definitions_depth,
                              inject_metadata=True,
                              parent=parent)

        # Cluster definitions with Tab, Group, and SubSetting
        clustered = ClusterDefinitions(definitions=definitions,
                                       cluster_settings=self.build_settings["Clustering"],
                                       logger=self.logger)

        definitions = clustered.get_definitions()

        container = FrameContainer(dict_depth=definitions_depth,
                                   logger=self.logger)

        # Merge each definition with the corresponding template and then build Frame
        for key, definition in definitions.items():
            # Merge definition with template
            templated_definition = self.templater.create_new_frame(definition)

            # Use the updated definition to build a frame
            frame = Frame(frame_builder=self,
                          template=templated_definition,
                          callback=callback,
                          logger=self.logger)

            # Add the frame to the frame container
            container.add_frame(key, frame)


        # Collect the paths and tabs of all the frames
        container.retrieve_information()

        return Widget(frame_container=container,
                      build_settings=self.build_settings)



