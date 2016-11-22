from .config import config
from .gotoclasscmd import ClassNavigatorGoToClassCommand
from .util import RegionList


class ClassNavigatorJumpFunctionCommand(ClassNavigatorGoToClassCommand):

    def run(self, edit, jump_next=True):
        filter_func = config[self.syntax_name].method_filter

        method_items = [
            item for item in self.view.symbols()
            if filter_func(item[1])
        ]

        self.status.clear()

        if method_items:
            self.filtered_regions, names = zip(*method_items)

            regions = RegionList(self.filtered_regions, self.view)
            index = regions.prev_region_index(self.current_line)

            self.save_start_position()
            if jump_next:
                self.jump_to(index + 1)
            elif regions.has_region(self.current_line):
                # located just on the region - jump to previous region
                self.jump_to(index - 1)
            else:
                # located in the middle of the region - jump to it's beginning
                self.jump_to(index)

        else:
            self.status.show('ClassNavigator: no function(s) found')
