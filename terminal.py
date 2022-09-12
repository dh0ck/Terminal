from burp import IBurpExtender, ITab
from javax.swing import JFrame, JSplitPane, JTable, JScrollPane, JPanel, BoxLayout, WindowConstants, JLabel, JMenuItem, JTabbedPane, JButton, JTextField, JTextArea, SwingConstants, JEditorPane, JComboBox, DefaultComboBoxModel, JFileChooser, ImageIcon, JCheckBox, JRadioButton, ButtonGroup, KeyStroke, JRadioButton 
from java.awt import BorderLayout, Dimension, FlowLayout, GridLayout, GridBagLayout, GridBagConstraints, Point, Component, Color  # quitar los layout que no utilice
from javax.swing.table import DefaultTableModel, DefaultTableCellRenderer, TableCellRenderer
import subprocess
import java
from   java.awt.event import ActionListener


class ComboBoxDemo( java.lang.Runnable, ActionListener ) :
    def run( self ) :
        frame = JFrame(
        'ComboBoxDemo',
        size = ( 200, 100 ),
        layout = FlowLayout(),
        defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JLabel( 'Pick one:' ) )
        choices = 'The,quick,brown,fox,jumped'.split( ',' )
        choices.extend( 'over,the,lazy,spam'.split( ',' ) )
        ComboBox = frame.add( JComboBox( choices ) )
        ComboBox.addActionListener( self )
        self.msg = frame.add( JLabel() )
        frame.setVisible( 1 )
    
    def actionPerformed( self, event ) :
        ComboBox = event.getSource()
        msg = 'Selection: ' + ComboBox.getSelectedItem()
        self.msg.setText( msg )

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.helpers
        callbacks.setExtensionName("Terminal")
        callbacks.addSuiteTab(self)
        global history
        history = self._callbacks.getProxyHistory()
        return

    def getTabCaption(self):
        return "Terminal"






    def getUiComponent(self):
        panel = JPanel()
        panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
        
        self.textarea1 = JTextArea("Editor")
        self.textarea2 = JTextArea("Output")

        self.splitted = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, JScrollPane(self.textarea1), JScrollPane(self.textarea2))
        panel.add(self.splitted)
        self.splitted.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.splitted.setResizeWeight(0.5)


        self.command_box = JTextField("Command")
        self.command_button = JButton("Run Command", actionPerformed = self.run_command)
        self.editor_button= JButton("Run Script")
        self.command_panel = JPanel()
        self.command_box.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.command_panel.add(JScrollPane(self.command_box))
        self.command_panel.add(self.command_button)
        self.command_panel.add(self.editor_button)


        self.combo_model = DefaultComboBoxModel()
        self.combo_model.addElement("OS")
        self.combo_model.addElement("Python")

        self.combo = JComboBox(self.combo_model)
        self.command_panel.add(self.combo)



        panel.add(self.command_panel)

        self.command_panel.setAlignmentX(Component.CENTER_ALIGNMENT)
        return panel

    def run_command(self, event):
        cmd = self.command_box.getText()
        output=subprocess.check_output(cmd, shell=True).decode('ISO-8859-1')
        self.textarea2.setText(output)