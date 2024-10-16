from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
import os
from datetime import datetime


class LogExplorer(BoxLayout):
    """
    LogExplorer is a UI component that displays a hierarchical view of log files
    from a directory, organized by year, month, day, and hour.

    Attributes:
        log_directory (str): Directory path containing log files.
        selected_files (list): List of files selected by the user in the TreeView.
        on_files_selected (callable): Callback function triggered when files are selected.
        display_array (DisplayArray): Reference to the DisplayArray instance to update the UI.
    """
    
    log_directory = StringProperty()
    selected_files = ListProperty()
    on_files_selected = ObjectProperty(None)  # Callback function

    def __init__(self, log_directory, display_array, **kwargs):
        """
        Initialize the LogExplorer widget.
        
        Args:
            log_directory (str): The directory where the log files are located.
            display_array (DisplayArray): The UI component that will display the log data.
            **kwargs: Additional keyword arguments for Kivy's BoxLayout initializer.
        """
        super(LogExplorer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.display_array = display_array

        # ScrollView to hold the TreeView
        self.scroll_view = ScrollView(do_scroll_y=True, size_hint=(1, 1))
        self.treeview = TreeView(
            root_options=dict(text="Dossier"),
            hide_root=True,
            indent_level=4,
            size_hint_y=None
        )
        self.treeview.bind(minimum_height=self.treeview.setter('height'))
        self.scroll_view.add_widget(self.treeview)
        self.add_widget(self.scroll_view)

        Window.bind(on_mouse_scroll=self.on_mouse_scroll)

        # If a log directory is provided, populate the treeview
        if self.log_directory:
            self.populate_treeview(self.log_directory)

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
        Update the log directory and refresh the tree view.
        
        Args:
            new_directory (str): The new log directory path to explore.
        """
        self.log_directory = new_directory
        self.populate_treeview(new_directory)

    def populate_treeview(self, log_directory):
        """
        Populate the TreeView with log files from the specified directory,
        organizing them by year, month, day, and hour.

        Args:
            log_directory (str): The directory containing log files.
        """
        if not os.path.exists(log_directory):
            return

        # Clear existing nodes in the tree view
        self.treeview.clear_widgets()

        # Add root node for "Logs"
        root_node = self.treeview.add_node(TreeViewLabel(text="Logs", size_hint_y=None, height=25))

        nodes = {}

        # Traverse the log directory and add nodes to the tree view
        for root, dirs, files in os.walk(log_directory):
            if not files:
                continue

            # Sort files by modification time, descending
            files.sort(key=lambda f: os.path.getmtime(os.path.join(root, f)), reverse=True)

            for file in files:
                file_path = os.path.join(root, file)
                file_date = self.get_file_date(file_path)

                year = str(file_date.year)
                month = file_date.strftime('%B')
                day = str(file_date.day)
                hour = str(file_date.hour) + ":00"

                # Create or retrieve year, month, day, and hour nodes
                year_node = nodes.get(year) or self.get_or_create_node(year, parent=root_node)
                month_key = f"{year}/{month}"
                month_node = nodes.get(month_key) or self.get_or_create_node(month, parent=year_node)
                day_key = f"{month_key}/{day}"
                day_node = nodes.get(day_key) or self.get_or_create_node(day, parent=month_node)
                hour_key = f"{day_key}/{hour}"
                hour_node = nodes.get(hour_key) or self.get_or_create_node(hour, parent=day_node)

                nodes.update({year: year_node, month_key: month_node, day_key: day_node, hour_key: hour_node})

                # Add the file to the tree view under the appropriate hour
                formatted_time = file_date.strftime('%H:%M')
                file_node = self.treeview.add_node(TreeViewLabel(text=formatted_time, size_hint_y=None, height=25),
                                                   parent=hour_node)
                file_node.file_path = file_path
                file_node.bind(on_touch_down=self.on_file_click)

    def get_file_date(self, file_path):
        """
        Get the last modification date of a file.

        Args:
            file_path (str): Path to the file.

        Returns:
            datetime: The modification date of the file.
        """
        file_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(file_time)

    def get_or_create_node(self, text, parent=None):
        """
        Retrieve an existing node with the given text under the specified parent.
        If it does not exist, create a new node.

        Args:
            text (str): The label text for the node.
            parent (TreeViewNode): The parent node.

        Returns:
            TreeViewLabel: The existing or newly created node.
        """
        for node in self.treeview.iterate_all_nodes():
            if node.text == text and node.parent == parent:
                return node
        return self.treeview.add_node(TreeViewLabel(text=text, size_hint_y=None, height=25), parent=parent)

    def colorize(self):
        """
        Update the color of TreeView nodes based on their selection state.
        """
        for node in self.treeview.iterate_all_nodes():
            if hasattr(node, 'file_path'):
                if node.file_path in self.selected_files:
                    node.odd_color = [.5, .5, .5, 1]
                    node.even_color = [.5, .5, .5, 1]
                else:
                    node.even_color = node.base_even_color
                    node.odd_color = node.base_odd_color

    def on_file_click(self, instance, touch):
        """
        Handle file selection when a TreeView node is clicked.

        Args:
            instance (TreeViewLabel): The clicked node instance.
            touch (Touch): Touch event information.
        """
        if instance.collide_point(*touch.pos):
            if os.path.isfile(instance.file_path):
                if 'ctrl' in Window.modifiers:  # Handle multi-selection with Ctrl key
                    self.selected_files.append(instance.file_path)
                else:
                    self.selected_files = [instance.file_path]
                self.colorize()
                self.display_array.updateTable(self.selected_files)

    def parseAndDisplay(self, selected_files):
        """
        Parse and display the selected log files in the DisplayArray component.
        
        Args:
            selected_files (list of str): List of selected file paths.
        """
        self.display_array.updateTable(selected_files)
