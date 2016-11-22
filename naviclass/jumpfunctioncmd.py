from .config import config
from .gotoclasscmd import ClassNavigatorGoToClassCommand
from .util import RegionList


class ClassNavigatorJumpFunctionCommand(ClassNavigatorGoToClassCommand):

    def run(self, edit, jump_next=True):
        method_items = [
            item for item in self.view.symbols()
            if config[self.syntax_name].is_function(item[1])
        ]

        self.status.clear()

        if method_items:
            self.filtered_regions, names = zip(*method_items)

            regions = RegionList(self.filtered_regions, self.view)
            index = regions.prev_region_index(self.current_line)

            self.save_start_position()
            if jump_next:
                self.jump_to(
                    index + 1,
                    cursor_position=self.find_function_name(index + 1))
            elif regions.has_region(self.current_line):
                # located just on the region - jump to previous region
                self.jump_to(
                    index - 1,
                    cursor_position=self.find_function_name(index - 1))
            else:
                # located in the middle of the region - jump to it's beginning
                self.jump_to(
                    index,
                    cursor_position=self.find_function_name(index))

        else:
            self.status.show('ClassNavigator: no function(s) found')

    def find_function_name(self, region_index):
        """Return index of function name in the string of provided region."""
        if region_index < 0 or region_index >= len(self.filtered_regions):
            return 0

        line_str = self.view.substr(self.filtered_regions[region_index])
        return config[self.syntax_name].index_of_function_name(line_str)
