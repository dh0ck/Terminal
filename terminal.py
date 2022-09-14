from burp import IBurpExtender, ITab
from javax.swing import JFrame, JSplitPane, JTable, JScrollPane, JPanel, BoxLayout, WindowConstants, JLabel, JMenuItem, JTabbedPane, JButton, JTextField, JTextArea, SwingConstants, JEditorPane, JComboBox, DefaultComboBoxModel, JFileChooser, ImageIcon, JCheckBox, JRadioButton, ButtonGroup, KeyStroke, JRadioButton 
from java.awt import BorderLayout, Dimension, FlowLayout, GridLayout, GridBagLayout, GridBagConstraints, Point, Component, Color  # quitar los layout que no utilice
from javax.swing.table import DefaultTableModel, DefaultTableCellRenderer, TableCellRenderer
import subprocess
import java
import sys
from   java.awt.event import ActionListener


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
        panel.setLayout(GridBagLayout())
        
        #panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
        
        self.textarea1 = JTextArea()
        self.textarea2 = JTextArea()

        self.editor = JPanel()
        self.editor.setLayout(BoxLayout(self.editor, BoxLayout.Y_AXIS))
        self.editor_label = JLabel("Editor")
        self.editor_label.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.editor.add(self.editor_label)
        self.editor.add(JScrollPane(self.textarea1))
        
        self.output = JPanel()
        self.output.setLayout(BoxLayout(self.output, BoxLayout.Y_AXIS))
        self.output_label = JLabel("Output")
        self.output_label.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.output.add(self.output_label)
        self.output.add(JScrollPane(self.textarea2))
        self.splitted = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, self.editor, self.output)
        

        c = GridBagConstraints()
        c.gridy = 0
        c.gridx = 0
        c.weighty = 2
        c.fill = GridBagConstraints.BOTH
        panel.add(self.splitted,c)
        self.splitted.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.splitted.setResizeWeight(0.5)


        self.command_panel = JPanel()
        self.command_panel.setLayout(GridBagLayout())
        

        self.command_box = JTextField("Command")
        #self.command_box.setAlignmentX(Component.CENTER_ALIGNMENT)
        self.command_button = JButton("Run Command", actionPerformed = self.run_command)
        self.editor_button= JButton("Run Script", actionPerformed = self.run_script)
        self.combo_model = DefaultComboBoxModel()
        self.combo_model.addElement("OS")
        self.combo_model.addElement("Python")
        self.combo = JComboBox(self.combo_model)


        c.gridx = 3
        
        c.fill = GridBagConstraints.HORIZONTAL
        c.weighty = 0
        self.command_panel.add(self.combo, c)

        c.gridx = 2
        self.command_panel.add(self.editor_button, c)

        c.gridx = 1
        c.fill = GridBagConstraints.HORIZONTAL
        self.command_panel.add(self.command_button, c)
        
        c.gridx = 0
        c.weightx = 1
        c.fill = GridBagConstraints.HORIZONTAL
        self.command_panel.add(JScrollPane(self.command_box),c)


        c.gridy += 1


        panel.add(self.command_panel, c)

        return panel

    def run_command(self, event):
        self.command_type = self.combo.getSelectedItem()

        self.cmd = self.command_box.getText()
        if self.command_type == 'OS':
            output = subprocess.check_output(self.cmd, shell=True).decode('ISO-8859-1')
            self.textarea2.setText(output)
        elif self.command_type == 'Python':

            try:
                cmd_output=subprocess.check_output(['python','-c',self.cmd],shell=True)
            except:
                try:
                    cmd_output=subprocess.check_output(['python3','-c',self.cmd],shell=True)
                except:
                    found = False
                    for path in jython_paths:
                        if '.jar' in path:
                            path = path.split('.jar')[0] + '.jar'
                            cmd_output=subprocess.check_output(['java','-jar',path,'-c',self.cmd],shell=True)
                            found = True
                            break
                    if not found:
                        
                        try:
                            f = open("selected_jython_path.txt","r")
                            path = f.read()
                            f.close()
                            cmd_output=subprocess.check_output(['java','-jar',path,'-c',self.cmd],shell=True)
                        except:
                            fc = JFileChooser()
                            result = fc.showOpenDialog( None )
                            if result == JFileChooser.APPROVE_OPTION :
                                path = str(fc.getSelectedFile())
    
                            f = open("selected_jython_path.txt","w")
                            f.write(path)
                            f.close()
    
                            cmd_output=subprocess.check_output(['java','-jar',path,'temp.py'],shell=True)
        self.textarea2.setText(str(cmd_output))



    def run_script(self, event):
        script = self.textarea1.getText()
        f = open("temp.py","w")
        f.write(script)
        f.close()
        jython_paths = sys.path


        try:
            #raise Exception("asfd") # estas exception son para probar los except
            script_output=subprocess.check_output(['python','temp.py'],shell=True)
        except:
            try:
                #raise Exception("asd") # estas exception son para probar los except
                script_output=subprocess.check_output(['python3','temp.py'],shell=True)
            except:
                found = False
                for path in jython_paths:
                    if '.jar' in path:
                        # esto es un poco chapuza, no se si siempre funcionara
                        path = path.split('.jar')[0] + '.jar'
                        script_output=subprocess.check_output(['java','-jar',path,'temp.py'],shell=True)
                        found = True
                        break
                if not found:
                    
                    try:
                        # try to use previously selected jython path. If never set, it will ask for it
                        f = open("selected_jython_path.txt","r")
                        path = f.read()
                        f.close()
                        script_output=subprocess.check_output(['java','-jar',path,'temp.py'],shell=True)
                    except:
                        fc = JFileChooser()
                        result = fc.showOpenDialog( None )
                        if result == JFileChooser.APPROVE_OPTION :
                            path = str(fc.getSelectedFile())

                        f = open("selected_jython_path.txt","w")
                        f.write(path)
                        f.close()

                        script_output=subprocess.check_output(['java','-jar',path,'temp.py'],shell=True)
        self.textarea2.setText(script_output)