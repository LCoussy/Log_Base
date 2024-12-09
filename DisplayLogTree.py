from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from FilterFiles import FilterFiles  # Import the new class

class LogExplorer(BoxLayout):
    """
    DisplayLogsTree is a UI component that handles displaying a hierarchical view
    of log files using a TreeView structure.
    """

    log_directory = StringProperty()
    selected_files = ListProperty()
    on_files_selected = ObjectProperty(None)  # Callback function triggered when files are selected

    def __init__(self, log_directory, display_array, **kwargs):
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
        self.display_array = display_array
        self.filter_files = FilterFiles()

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

    def populate_treeview(self):
        """
        Populate the TreeView with log files organized by year, month, day, and hour.

        This method retrieves the file organization from FilterFiles and builds the TreeView structure.
        """
        self.treeview.clear_widgets()
        root_node = self.treeview.add_node(TreeViewLabel(text="Logs", size_hint_y=None, height=25))

        # Get the organized file structure
        file_hierarchy = self.filter_files.organize_files_by_date(self.log_directory)

        # Recursively add nodes to the tree
        self.add_nodes(file_hierarchy, parent_node=root_node)

    def add_nodes(self, hierarchy, parent_node):
        """
        Recursively add nodes to the TreeView based on the file hierarchy.

        Args:
            hierarchy (dict): The hierarchical structure of files.
            parent_node (TreeViewNode): The parent node to add children to.
        """
        for key, value in hierarchy.items():
            node = self.treeview.add_node(TreeViewLabel(text=key, size_hint_y=None, height=25), parent=parent_node)
            
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
            parent=parent_node
        )
        file_node.file_path = file_info["file_path"]
        file_node.bind(on_touch_down=self.on_file_click)

    def colorize(self):
        """
        Update the color of TreeView nodes based on their selection state.
        """
        for node in self.treeview.iterate_all_nodes():
            if hasattr(node, 'file_path'):
                is_selected = node.file_path in self.selected_files
                color = [.5, .5, .5, 1] if is_selected else getattr(node, 'base_even_color', [1, 1, 1, 1])
                node.odd_color = node.even_color = color

    def on_file_click(self, instance, touch):
        """
        Handle file selection when a TreeView node is clicked.

        Args:
            instance (TreeViewLabel): The clicked node instance.
            touch (Touch): Touch event information.
        """
        if instance.collide_point(*touch.pos) and hasattr(instance, 'file_path'):
            if 'ctrl' in Window.modifiers:  # Multi-select with Ctrl key
                if instance.file_path not in self.selected_files:
                    self.selected_files.append(instance.file_path)
            else:  # Single select
                self.selected_files = [instance.file_path]

            self.colorize()  # Update the color of selected files
            self.display_array.updateTable(self.selected_files)  # Update the display with selected files
