from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from FilterFiles import FilterFiles  # Import the new class
import pprint

class LogExplorer(BoxLayout):
    """
    DisplayLogsTree is a UI component that handles displaying a hierarchical view
    of log files using a TreeView structure.
    """

    log_directory = StringProperty()
    selected_files = ListProperty()
    on_files_selected = ObjectProperty(None)  # Callback function triggered when     files are selected

    # def __init__(self, log_directory, display_array, **kwargs):
    def __init__(self, log_directory, on_file_selected=None, **kwargs):
        """
        Initialize the DisplayLogsTree widget.

        Args:
            log_directory (str): The directory where the log files are located.
            display_array (DisplayArray): The UI component that will display the log data.
            **kwargs: Additional keyword arguments for Kivy's BoxLayout initializer.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        # self.display_array = display_array
        self.filter_files = FilterFiles()
        self.on_file_selected = on_file_selected


        # Set up the ScrollView for vertical scrolling
        self.scroll_view = ScrollView(do_scroll_y=True, size_hint=(1, 1))

        # Set up the TreeView to display the log files in a hierarchical manner
        self.treeview = TreeView(
            root_options=dict(text="Dossier"),
            hide_root=True,
            indent_level=4,
            size_hint_y=None
        )
        self.treeview.bind(minimum_height=self.treeview.setter('height'))
        self.scroll_view.add_widget(self.treeview)
        self.add_widget(self.scroll_view)

        # Bind mouse scroll event for controlling the scroll view
        Window.bind(on_mouse_scroll=self.on_mouse_scroll)

        # If the log directory is provided, populate the treeview with data
        if log_directory:
            self.update_directory(log_directory)

    def on_mouse_scroll(self, window, x, y, scroll_x, scroll_y):
        """
        Handle mouse scroll events for the scroll view.

        Args:
            window (Window): The Kivy window instance.
            x, y (int): Coordinates of the mouse pointer.
            scroll_x, scroll_y (float): Scroll offset in x and y directions.
        """
        if self.scroll_view:
            self.scroll_view.scroll_y += scroll_y / 10.0

    def update_directory(self, new_directory):
        """
        Update the log directory and refresh the tree view with new data.

        Args:
            new_directory (str): The new log directory path to explore.
        """
        self.log_directory = new_directory
        self.populate_treeview()

    def create_file_hierarchy(self, log_directory):
        """
        Create a hierarchical structure of log files based on year, month, day, and hour.

        Args:
            log_directory (str): The directory where the log files are located.

        Returns:
            dict: A hierarchical structure of log files organized by year, month, day, and hour.
        """
        file_hierarchy = {}
        pattern_filename = re.compile(r'')
        for file in self.filter_files.get_files(log_directory):
            file_info = self.filter_files.get_file_info(file)
            year = file_info["year"]
            month = self.get_month(file_info["month"])
            day = file_info["day"]
            hour = file_info["hour"]

            if year not in file_hierarchy:
                file_hierarchy[year] = {}
            if month not in file_hierarchy[year]:
                file_hierarchy[year][month] = {}
            if day not in file_hierarchy[year][month]:
                file_hierarchy[year][month][day] = {}
            if hour not in file_hierarchy[year][month][day]:
                file_hierarchy[year][month][day][hour] = []

            file_hierarchy[year][month][day][hour].append(file_info)

        return file_hierarchy

    def populate_treeview(self):
        """
        Populate the TreeView with log files organized by year, month, day, and hour.

        This method retrieves the file organization from FilterFiles and builds the TreeView structure.
        """
        self.treeview.clear_widgets()
        root_node = self.treeview.add_node(TreeViewLabel(text="Logs", size_hint_y=None, height=25))

        # Get the organized file structure
        file_hierarchy = self.filter_files.organize_files_by_date(self.log_directory)
        # print(self.log_directory)

        # Recursively add nodes to the tree
        self.add_nodes(file_hierarchy, parent_node=root_node)
        # for key, value in file_hierarchy.items():
        #     print(f"{key}: {value}\n")
        # pprint.pprint(file_hierarchy)

    def add_nodes(self, hierarchy, parent_node):
        """
        Recursively add nodes to the TreeView based on the file hierarchy.

        Args:
            hierarchy (dict): The hierarchical structure of files.
            parent_node (TreeViewNode): The parent node to add children to.
        """
        for key, value in hierarchy.items():
            # print("key: ", key)
            # print("value: ", value)
            node = self.treeview.add_node(TreeViewLabel(text=key, size_hint_y=None, height=25), parent=parent_node)
            node.base_even_color = node.even_color
            node.base_odd_color = node.odd_color
            node.file_path = key  # Set file_path for parent nodes
            node.bind(on_touch_down=self.on_parent_file_click)

            if isinstance(value, dict):
                # Recursively add child nodes
                self.add_nodes(value, parent_node=node)
            elif isinstance(value, list):
                # Add file nodes
                for file_info in value:
                    self.add_file_node(file_info, parent_node=node)

    def add_file_node(self, file_info, parent_node):
        """
        Add a file node to the TreeView under the specified parent node.

        Args:
            file_info (dict): Information about the file (path and formatted time).
            parent_node (TreeViewNode): The parent node where the file will be added.
        """
        file_node = self.treeview.add_node(
            TreeViewLabel(text=file_info["formatted_time"], size_hint_y=None, height=25),
            parent=parent_node,
        )
        file_node.base_even_color = file_node.even_color
        file_node.base_odd_color = file_node.odd_color
        file_node.file_path = file_info["file_path"]
        file_node.bind(on_touch_down=self.on_leaf_file_click)

    def colorize(self):
        """
        Update the color of TreeView nodes based on their selection state.
        """
        # for node in self.treeview.iterate_all_nodes():
        #     if hasattr(node, 'file_path'):
        #         is_selected = node.file_path in self.selected_files
        #         color = [.5, .5, .5, 1] if is_selected else getattr(node, 'base_even_color', [1, 1, 1, 1])
        #         node.odd_color = node.even_color = color

        for node in self.treeview.iterate_all_nodes():
            if hasattr(node, 'file_path'):
                if node.file_path in self.selected_files:
                    self.treeview.deselect_node(node)
                    node.odd_color = [.5, .5, .5, 1]
                    node.even_color = [.5, .5, .5, 1]
                else:
                    node.even_color = node.base_even_color
                    node.odd_color = node.base_odd_color
        # Update parent nodes based on the selection state of their children
        for node in self.treeview.iterate_all_nodes():
            if not node.is_leaf:
                child_selected = any(child.file_path in self.selected_files for child in self.treeview.iterate_all_nodes(node) if hasattr(child, 'file_path'))
                if child_selected:
                    node.odd_color = [.3, .3, .3, 1]
                    node.even_color = [.3, .3, .3, 1]
                else:
                    node.even_color = node.base_even_color
                    node.odd_color = node.base_odd_color


    def on_leaf_file_click(self, instance, touch):
        """
        Handle file selection when a TreeView node is clicked.

        Args:
            instance (TreeViewLabel): The clicked node instance.
            touch (Touch): Touch event information.
        """
        if instance.collide_point(*touch.pos) and hasattr(instance, 'file_path'):
            if 'alt' in Window.modifiers:  # Multi-select with Ctrl key
                if instance.file_path not in self.selected_files:
                    self.selected_files.append(instance.file_path)
            else:  # Single select
                self.selected_files = [instance.file_path]

            self.colorize()

            if self.on_file_selected:
                self.on_file_selected(self.selected_files)

    def on_parent_file_click(self, instance, touch):
        """
        Handle file selection when a parent node is clicked.

        Args:
            instance (TreeViewLabel): The clicked node instance.
            touch (Touch): Touch event information.
        """
        self.selected_files = []
        if instance.collide_point(*touch.pos) and hasattr(instance, 'file_path'):
            actual_node = self.treeview.get_selected_node()
            if not actual_node.is_leaf:
                for node in self.treeview.iterate_all_nodes(actual_node):
                    if node.is_leaf:
                        self.selected_files.append(node.file_path)
            self.colorize()

            if self.on_file_selected:
                self.on_file_selected(self.selected_files)