from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox, QLabel, QToolButton,  QSpinBox, QPushButton, QFrame,QProxyStyle
from generalFunctions import GeneralFunctions


class Proxy(QProxyStyle):
    def subControlRect(self, control, opt, subControl, widget=None):
        rect = super().subControlRect(control, opt, subControl, widget)
        if control == self.CC_SpinBox:
            if subControl in (self.SC_SpinBoxUp, self.SC_SpinBoxDown):
                rect.setLeft(opt.rect.width() - 20)
            elif subControl == self.SC_SpinBoxEditField:
                rect.setRight(opt.rect.width())
        return rect


class JbadonaiStyleSheetCode:
    def __init__(self):
        pass

    def reset_styles(self, parent):
        style_sb_20 = """
        *{
        border: none;
        margin:0;
        padding:0;
        }

        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
        }       
        
        
        QScrollBar:horizontal{
        height:20px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0.994318, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:10px;
        }
        
        QScrollBar:vertical{
        width:20px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:10px;
        }

        QScrollBar::handle:horizontal {
        background-color: qlineargradient(spread:pad, x1:0, y1:0.943182, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:3px;
        border-radius: 5px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::handle:vertical  {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:3px;
        border-radius: 5px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background-color:gray;
            color:black;
            }
            
        """

        style_sb_10 = """
        *{
        border: none;
        margin:0;
        padding:0;
        }

        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
        }       
        
        
        QScrollBar:horizontal{
        height:13px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0.994318, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:5px;
        }
        
        QScrollBar:vertical{
        width:13px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:5px;
        }

        QScrollBar::handle:horizontal {
        background-color: qlineargradient(spread:pad, x1:0, y1:0.943182, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:2px;
        border-radius: 3px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::handle:vertical  {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:2px;
        border-radius: 3px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background-color:gray;
            color:black;
            }
            
        """

        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            parent.setStyleSheet(style_sb_20)
        else:
            parent.setStyleSheet(style_sb_10)

    def context_menu_stylesheet(self):
        style = """
            QMenu{
               color: rgb(0, 255, 127);
               background-color: rgb(10, 10, 10);
               border-left: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-right: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-top: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-bottom: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               margin-left:2px;
               padding-left:10px;
               font:9pt;
            }

           QMenu::item::selected{
               color: white;
               background-color: blue;
               font:9pt;
               padding-left:13px;
           }
           
           QMenu::separator{
            background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
           }

        """
        return style

    def scrollbar_stylesheet(self):
        style = """
        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal  {
        height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
        }       
        
        
        QScrollBar:horizontal{
        height:20px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0.994318, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:10px;
        }
        
        QScrollBar:vertical{
        width:20px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.181818 rgba(197, 197, 197, 255), stop:0.829545 rgba(213, 213, 213, 255), stop:0.98 rgba(97, 97, 97, 255), stop:1 rgba(0, 0, 0, 0));;
        border-radius:10px;
        }

        QScrollBar::handle:horizontal {
        background-color: qlineargradient(spread:pad, x1:0, y1:0.943182, x2:0, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:4px;
        border-radius: 5px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::handle:vertical  {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(90, 90, 90, 255), stop:0.5 rgba(173, 173, 173, 255), stop:0.545455 rgba(176, 176, 176, 255), stop:0.943182 rgba(91, 91, 91, 255));;
        margin:4px;
        border-radius: 5px;       
        border: 1px solid rgb(35,35,35);
        }
        
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background-color:gray;
            color:black;
            }
        """
        return style

    def button_no_border(self, button_to_style, font_size=10, font_color="gray", background="transparent", icon_size=20, padding="2", margin=2):

        def style_object(button):
            objectName = button.objectName()
            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            font-size: {font_size}pt;
            color: {font_color};
            padding: {realPadding};
            margin: {realMarging};
            background-color: {background};     
            border: none ;
            """

            style = f"#{objectName}" + "{" + f"{styleCode}" + "}"

            button.setIconSize(QSize(icon_size, icon_size))
            button.setStyleSheet(style)

        for button in button_to_style:
            style_object(button)

    def button_with_border(self, button_to_style, font_size=10, font_color="gray", background="transparent", icon_size=20, padding="2", margin=2, b_size=2, b_style="solid", b_color="black", b_radius=0):

        def style_object(button):
            objectName = button.objectName()
            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            font-size: {font_size}pt;
            color: {font_color};
            padding: {realPadding};
            margin: {realMarging};
            background-color: {background};     
            border: {b_size}px {b_style} {b_color};
            border-radius: {b_radius};
             
            """

            style = f"#{objectName}" + "{" + f"{styleCode}" + "}"

            button.setIconSize(QSize(icon_size, icon_size))
            button.setStyleSheet(style)

        for button in button_to_style:
            style_object(button)

    def container_no_border(self, object_to_style, margin="0", padding="0", font_size=12, font_color="gray", background="transparent"):

        def style_object(obj):
            objectName = obj.objectName()

            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            padding: {realPadding};
            margin: {realMarging};
            font-size: {font_size}pt;
            color: {font_color};
            background-color:{background};
            """
            style = f"#{objectName}" + "{" + f"{styleCode}" + "}"
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)

    def container_with_border(self, object_to_style, margin="0", padding="0",font_color="white", font_size=12, background="transparent", b_size=2, b_style="solid", b_color="black", b_radius=0, ba=True, bt=False, bl=False, bb=False, br=False):

        def style_object(obj):
            objectName = obj.objectName()

            def get_border_code():
                borderCode = ""
                borderTop = f"{b_size}px {b_style} {b_color}"
                borderRight = f"{b_size}px {b_style} {b_color}"
                borderBottom = f"{b_size}px {b_style} {b_color}"
                borderLeft = f"{b_size}px {b_style} {b_color}"

                if ba is True:
                    borderCode = f"border: {b_size}px {b_style} {b_color};"
                else:
                    if bt is True:
                        borderCode += f"border-top: {borderTop}; \n"

                    if br is True:
                        borderCode += f"border-right: {borderRight}; \n"

                    if bb is True:
                        borderCode += f"border-bottom: {borderBottom}; \n"

                    if bl is True:
                        borderCode += f"border-left: {borderLeft}; \n"

                return borderCode

            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            padding: {realPadding};
            margin: {realMarging};
            font-size: {font_size}pt;
            color: {font_color};
            {get_border_code()}
            border-radius: {b_radius};
            background-color: {background};
            """
            style = f"#{objectName}" + "{" + f"{styleCode}" + "}"
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)

    def options_style(self, object_to_style, margin="0", padding="0", font_size=8, font_color="gray", hover_color="white"):

        def style_object(obj):
            objectName = obj.objectName()

            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            padding: {realPadding};
            margin: {realMarging};
            font-size: {font_size}pt;
            """

            hoverCode = f"""    
                color:{hover_color} 
                    """
            hover = f"#{objectName}:hover" + "{" + f"{hoverCode}" + "}"

            style = f"#{objectName}" + "{" + f"{styleCode}" + "}" + "\n" + hover
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)

    def append_with_hover(self, object_to_style, font_color="gray", background="transparent",border=False, b_size=1, b_style="solid", b_color="black", b_radius=0):

        def style_object(obj):
            objectName = obj.objectName()

            styleCode = obj.styleSheet()

            if border is False:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};             
                    """
            else:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};
                    border: {b_size}px {b_style} {b_color};
                    border-radius: {b_radius};
                        """
            hover = f"#{objectName}:hover" + "{" + f"{hoverCode}" + "}"

            style =  f"{styleCode}"  + "\n" + hover
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)

    def append_with_pressed(self, object_to_style, font_color="gray", font_size=11, background="transparent",border=False, b_size=2, b_style="solid", b_color="black", b_radius=0):

        def style_object(obj):
            objectName = obj.objectName()

            styleCode = obj.styleSheet()

            if border is False:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};     
                    font-size:{font_size}pt;  
                          
                    """
            else:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};
                    border: {b_size}px {b_style} {b_color};
                    border-radius: {b_radius};
                    font-size:{font_size}pt;     
                        """
            hover = f"#{objectName}:pressed" + "{" + f"{hoverCode}" + "}"

            style =  f"{styleCode}"  + "\n" + hover
            obj.setStyleSheet(style)


        for obj in object_to_style:
            style_object(obj)

    def append_with_special(self, object_to_style,special="indicator", font_color="gray", margin="0", padding="0", background="transparent",border=False, b_size=2, b_style="solid", b_color="black", b_radius=0):

        def style_object(obj):
            objectName = obj.objectName()
            styleCode = obj.styleSheet()

            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            if border is False:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};   
                    padding: {realPadding};
                    margin: {realMarging};     
                    """
            else:
                hoverCode = f"""    
                    color:{font_color};
                    background-color: {background};
                    border: {b_size}px {b_style} {b_color};
                    border-radius: {b_radius};
                    padding: {realPadding};
                    margin: {realMarging};
                        """
            hover = f"#{objectName}::{special}" + "{" + f"{hoverCode}" + "}"

            style = f"{styleCode}" + "\n" + hover
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)

    def label_heading_style(self, object_to_style, margin="0", padding="0", font_size=8, font_color="gray"):

        def style_object(obj):
            objectName = obj.objectName()

            pad = str(padding).split(",")
            mar = str(margin).split(",")
            realPadding = ""
            realMarging = ""

            for p in pad:
                realPadding += f"{p}px "

            for m in mar:
                realMarging += f"{m}px "

            styleCode = f"""
            padding: {realPadding};
            margin: {realMarging};
            font-size: {font_size}pt;
            color: {font_color};
            """

            style = f"#{objectName}" + "{" + f"{styleCode}" + "}"
            obj.setStyleSheet(style)

        for obj in object_to_style:
            style_object(obj)


class ColorScheme():
    def __init__(self):
        self._theme = {}

    def bg_color(self, *args):
        # print("args: ", args)
        if len(args) == 1:
            return f"rgb({args[0]},{args[0]},{args[0]})"

        if len(args) == 3:
            return f"rgb({args[0]},{args[1]},{args[2]})"

    def dark_theme(self):
        color_radial_gradient = "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0))"
        color_primary_green = "rgb(0,255,127)"
        color_primary_black = "black"
        color_pale_white = "rgb(200,200,200)"
        primary_border_color = "gray"
        color_transparent = "transparent"
        color_bright_yellow = "yellow"
        color_bright_white = "white"
        color_bright_blue = "blue"
        color_pale_blue = "rgba(16,88,145,255)"
        color_bright_red = "red"
        color_blue_highlight = "blue"


        color_title_bar_bg = self.bg_color(10)
        color_tool_bar_bg = self.bg_color(15)
        color_central = self.bg_color(75)
        color_button_hover = self.bg_color(65)
        color_button_pressed = self.bg_color(45)
        color_panel_bg = self.bg_color(25)
        color_bright_hover = self.bg_color(240)

        self._theme['color_radial_gradient'] = color_radial_gradient
        self._theme['color_primary_green'] = color_primary_green
        self._theme['color_primary_black'] = color_primary_black
        self._theme['color_pale_white'] = color_pale_white
        self._theme['primary_border_color'] = primary_border_color
        self._theme['color_transparent'] = color_transparent
        self._theme['color_bright_yellow'] = color_bright_yellow
        self._theme['color_bright_white'] = color_bright_white
        self._theme['color_bright_blue'] = color_bright_blue
        self._theme['color_pale_blue'] = color_pale_blue
        self._theme['color_bright_red'] = color_bright_red

        self._theme['color_title_bar_bg'] = color_title_bar_bg
        self._theme['color_tool_bar_bg'] = color_tool_bar_bg
        self._theme['color_central'] = color_central
        self._theme['color_button_hover'] = color_button_hover
        self._theme['color_button_pressed'] = color_button_pressed
        self._theme['color_panel_bg'] = color_panel_bg
        self._theme['color_bright_hover'] = color_bright_hover
        self._theme['color_blue_highlight'] = color_blue_highlight

        return self._theme

    def light_theme(self):
        color_radial_gradient = "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0))"
        color_primary_green = "black"
        color_primary_black = "black"
        color_pale_white = "rgb(200,200,200)"
        primary_border_color = "white"
        color_transparent = "transparent"
        color_bright_yellow = "blue"
        color_bright_white = "black"
        color_bright_blue = "blue"
        color_bright_red = "red"

        color_title_bar_bg = self.bg_color(180, 92, 24)
        color_tool_bar_bg = self.bg_color(19, 87, 20)
        color_panel_bg = self.bg_color(180, 92, 24)
        color_central = self.bg_color(204,165,41)

        color_button_hover = self.bg_color(65)
        color_button_pressed = self.bg_color(45)

        color_bright_hover = self.bg_color(240)

        self._theme['color_radial_gradient'] = color_radial_gradient
        self._theme['color_primary_green'] = color_primary_green
        self._theme['color_primary_black'] = color_primary_black
        self._theme['color_pale_white'] = color_pale_white
        self._theme['primary_border_color'] = primary_border_color
        self._theme['color_transparent'] = color_transparent
        self._theme['color_bright_yellow'] = color_bright_yellow
        self._theme['color_bright_white'] = color_bright_white
        self._theme['color_bright_blue'] = color_bright_blue
        self._theme['color_bright_red'] = color_bright_red

        self._theme['color_title_bar_bg'] = color_title_bar_bg
        self._theme['color_tool_bar_bg'] = color_tool_bar_bg
        self._theme['color_central'] = color_central
        self._theme['color_button_hover'] = color_button_hover
        self._theme['color_button_pressed'] = color_button_pressed
        self._theme['color_panel_bg'] = color_panel_bg
        self._theme['color_bright_hover'] = color_bright_hover

        return self._theme


class VideoDownloaderStyleSheet():
    def __init__(self, myself, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']

    def _get_radio_radius(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            return 10
        else:
            return 7

    def _get_panel_width(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            return 150
        else:
            return 80

    def _get_titlebar_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 25
        elif sz.height > 800 and sz.height <=960:
            return 18
        else:
            return 17

    def _get_toolbar_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 800:
            return 20
        else:
            return 15

    def _get_add_new_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 800:
            return 40
        else:
            return 30

    # ==================================================

    def apply_stylesheet(self):
        self._style_initial_reset()
        self._style_centralwidget()
        self._style_titlebar(iconSize=self._get_titlebar_icon_size())
        self._style_toolbar(iconSize=self._get_toolbar_icon_size())
        self._style_add_new_panel(width_margin=self._get_panel_width(), radio_radius=self._get_radio_radius(), iconSize=self._get_add_new_icon_size())
        self._style_settings_panel()
        self._style_statistics_panel()
        self._style_download_area_panel()

    # ==================================================
    def _style_initial_reset(self):
        self.my_style.reset_styles(self.myself)

    def _style_centralwidget(self):
        self.my_style.container_no_border([self.myself.centralWidget()], background=self.color_central)

    def _style_titlebar(self, iconSize=25, borderRadius=10):
        self.my_style.container_with_border(object_to_style=(self.myself.frame_TitleBar,), background=self.color_title_bar_bg,
                                    font_color=self.color_primary_green, padding="5,5,5,5", ba=False, bt=True, b_size=1,
                                    bb=True, b_color=self.primary_border_color, b_radius=0)

        self.my_style.button_no_border([self.myself.buttonTitleIcon], icon_size=iconSize, padding=0, margin=0,
                                       background=self.color_transparent)

        self.my_style.container_no_border([self.myself.labelActivationStatus], font_color=self.color_bright_yellow,
                                       font_size=8)

        self.my_style.label_heading_style([self.myself.labelTitle], font_color=self.color_primary_green,font_size=11,
                                          margin="0,0,0,10")

        self.my_style.container_with_border([self.myself.frame_internet_speed], margin="0,5", padding="0,10",
                                            ba=False, bl=True, b_size=5, b_color=self.color_radial_gradient)

        self.my_style.container_no_border([self.myself.frame_internet_available], margin="0, 5")

        self.my_style.container_no_border([self.myself.labelInternetAvailable, self.myself .labelInternetSpeed],
                                          margin="0,5,0,0", font_size=8, font_color=self.color_primary_green)

        self.my_style.container_no_border([self.myself.textInternetSpeed], font_size=8,
                                          font_color=self.color_bright_yellow)

        self.my_style.container_no_border([self.myself.frame_connection_stats, self.myself.buttonInternetAvailable],
                                          margin="0,10,0,0")

        control_buttons = [self.myself.buttonClose, self.myself.buttonRestoreMaximize, self.myself.buttonMinimize]

        self.my_style.button_with_border(control_buttons, b_size=2, b_radius=borderRadius, b_color="rgb(125,125,125)",
                                         margin="0,5,5,5", padding=1, icon_size=iconSize)

        self.my_style.append_with_hover(control_buttons, background=self.primary_border_color,
                                        b_color=self.color_bright_white)

        self.my_style.append_with_pressed(control_buttons, b_color=self.color_bright_white)
        pass

    def _style_toolbar(self, iconSize=20, borderRadius=10):

        self.my_style.container_with_border([self.myself.frame_toolbar], background=self.color_tool_bar_bg, padding="3,10",
                                          ba=False, bb=True, b_size=2, b_color=self.primary_border_color)

        self.my_style.button_with_border([self.myself.buttonActivate], b_radius=borderRadius, padding="5", b_size=1,
                                         icon_size=iconSize, b_color=self.color_primary_green,
                                         background=self.color_bright_blue, font_color=self.color_bright_white)
        for button in self.myself.frame_settings.children():
            if type(button) == QPushButton:

                self.my_style.button_with_border([button], b_radius=borderRadius, padding="5", b_size=1, icon_size=iconSize)

                self.my_style.append_with_hover([button], b_size=1, background=self.color_button_hover,
                                                b_color=self.color_bright_white, b_radius=borderRadius)

                self.my_style.append_with_pressed([button], b_size=1, background=self.color_button_pressed,
                                                  b_color=self.color_bright_yellow, b_radius=borderRadius)

        for button in self.myself.frame_theme.children():
            if type(button) == QPushButton:

                self.my_style.button_with_border([button], b_radius=borderRadius, padding="5", b_size=1, icon_size=iconSize)

                self.my_style.append_with_hover([button], b_size=1, background=self.color_button_hover,
                                                b_color=self.color_bright_white, b_radius=borderRadius)

                self.my_style.append_with_pressed([button], b_size=1, background=self.color_button_pressed,
                                                  b_color=self.color_bright_yellow, b_radius=borderRadius)

        # self.frame_owner
        # self.textOwner
        self.my_style.container_with_border([self.myself.frame_owner], b_size=1, b_color=self.color_radial_gradient,
                                            ba=False, br=True, bl=True)
        self.my_style.container_no_border([self.myself.textOwner],font_color=self.primary_border_color, font_size=7)


        pass

    def _style_add_new_panel(self, width_margin=150, radio_radius=10, iconSize=40):

        self.my_style.container_with_border([self.myself.frame_addNew],margin=f"-15,{width_margin},10,{width_margin}",
                                            background=self.color_panel_bg, padding="15,5,10,25", b_size=2,
                                            b_style="solid", b_color=self.primary_border_color, b_radius=20,
                                            font_color=self.color_bright_white)

        self.my_style.container_with_border(object_to_style=[self.myself.textAddNewURL], margin="0,20,0,0", padding="5",
                                            background=self.color_pale_white,b_radius=10, font_size=9,
                                            font_color=self.color_primary_black)

        self.my_style.append_with_hover([self.myself.textAddNewURL],background=self.color_bright_hover)

        self.my_style.button_no_border(button_to_style=(self.myself.buttonAddNewDownload,), font_size=11,
                                       font_color=self.color_pale_white, icon_size=iconSize, padding="0, 10",
                                       margin="0,20,0,0")

        self.my_style.append_with_hover([self.myself.buttonAddNewDownload], border=True, background=self.color_button_hover,
                                        b_size=1, b_color=self.primary_border_color, b_radius=20,
                                        font_color=self.color_pale_white)

        self.my_style.append_with_pressed([self.myself.buttonAddNewDownload], border=True, background=self.color_button_pressed,
                                          font_size=10, b_size=1, b_color=self.primary_border_color, b_radius=20,
                                          font_color=self.primary_border_color)

        self.my_style.container_with_border([self.myself.groupBoxDownloadOption], font_color=self.color_pale_white,
                                            padding="30,0,0,10", ba=False, b_radius=0, b_size=5,
                                            b_color=self.color_radial_gradient, bl=True, font_size=8)

        self.my_style.container_no_border(object_to_style=(self.myself.radioButtonAudioDownload,
                                                           self.myself.radioButtonVideoDownload), padding=0,
                                          font_color=self.color_primary_green, font_size=9, margin=5)

        self.my_style.append_with_hover((self.myself.radioButtonAudioDownload, self.myself.radioButtonVideoDownload),
                                        font_color=self.color_bright_yellow)

        self.my_style.append_with_special((self.myself.radioButtonAudioDownload, self.myself.radioButtonVideoDownload),
                                          border=True, b_color=self.primary_border_color, b_size=1, b_radius=radio_radius,
                                          background=self.color_bright_yellow, special="indicator::checked")

        self.my_style.append_with_special((self.myself.radioButtonAudioDownload, self.myself.radioButtonVideoDownload),
                                          border=True, b_color=self.color_bright_white, b_size=1, b_radius=radio_radius,
                                          background=self.color_transparent, special="indicator::unchecked")

        self.my_style.label_heading_style((self.myself.labelFormat,), font_size=8, font_color=self.color_pale_white,
                                          margin="0,0,15,0")

        self.my_style.container_no_border([self.myself.comboBoxSelectFormat], background=self.color_pale_white,
                                          font_color=self.color_primary_black, padding=2, font_size=9)

        self.my_style.append_with_hover([self.myself.comboBoxSelectFormat], background=self.color_bright_hover,
                                        font_color=self.color_primary_black)

        self.my_style.container_with_border([self.myself.labelAddNewStatus], ba=False, bt=True, bb=True, b_size=5,
                                            b_color=self.color_radial_gradient, font_size=8, font_color=self.color_bright_yellow,
                                            background=self.color_panel_bg, padding=2)

        self.my_style.button_no_border((self.myself.buttonHideShowAddNew,), margin="0,10,0,0", icon_size=20)

        self.my_style.append_with_hover((self.myself.buttonHideShowAddNew,), background=self.color_button_hover, border=True,
                                        b_radius=10, b_size=1, b_color=self.primary_border_color)

    def _style_settings_panel(self):
        self.my_style.container_with_border([self.myself.frame_settings_head], ba=False, bb=True,
                                            b_color=self.color_radial_gradient, padding="0,0,5,0", b_size=8)

        self.my_style.container_no_border([self.myself.labelSettings],font_size=12,
                                          font_color=self.primary_border_color)

        self.my_style.container_with_border([self.myself.frame_main_settings], background=self.color_panel_bg,
                                            padding=3, b_size=2, ba=False, bl=True, b_color=self.primary_border_color)

        self.my_style.container_no_border([self.myself.scrollAreaSettings], background=self.color_transparent)

        for frame in self.myself.frame_settings_top.children():
            if type(frame) == QFrame:
                self.my_style.container_with_border([frame], margin="5,0", padding="10,5,10,0", ba=False, bb=True,
                                                    b_size=5, b_color=self.color_radial_gradient)

        for frame in self.myself.frame_settings_top.children():
            for child in frame.children():
                # styling only the checkbox in settings panel
                if type(child) == QCheckBox:
                    self.my_style.container_no_border([child], font_color=self.color_pale_white, font_size=9)
                    self.my_style.append_with_special(
                        object_to_style=(child,),
                        border=True, b_color=self.primary_border_color, b_size=1,  background=self.color_bright_yellow,
                        special="indicator::checked")

                    self.my_style.append_with_special(
                        object_to_style=(child,),
                        border=True, b_color=self.primary_border_color, b_size=1,  background=self.color_transparent,
                        special="indicator::unchecked")

                    self.my_style.append_with_special(
                        object_to_style=(child,),
                        border=False,  background=self.color_transparent, font_color=self.primary_border_color,
                        special="unchecked")

                # styling only the labels in settings panel
                if type(child) == QLabel:
                    if child.objectName() == "textDownloadLocation":
                        self.my_style.container_no_border([child], padding="5,1", font_size=9,
                                                          font_color=self.color_primary_green)
                    else:
                        self.my_style.container_no_border([child], padding="5,1", font_size=9,
                                                          font_color=self.primary_border_color)

                # styling only the labels in settings panel
                if type(child) == QToolButton:
                    self.my_style.container_no_border([child],  font_color=self.color_bright_white, margin="0,1,0,0",
                                                      font_size=9, background=self.primary_border_color)

                    self.my_style.append_with_hover([child], background=self.color_button_hover,
                                                    font_color=self.color_primary_green)

                    self.my_style.append_with_pressed([child], background=self.color_button_pressed,
                                                      font_color=self.color_primary_green)

                # styling all the spinbox in settings panel
                if type(child) == QSpinBox:
                    self.my_style.container_no_border([child],  background=self.color_pale_white,
                                                      font_color=self.color_primary_black, font_size=9, margin=0,
                                                      padding=5)

                    self.my_style.append_with_hover([child], background=self.color_bright_hover,
                                                    font_color=self.color_primary_black)

        # styling license panel
        self.my_style.container_with_border([self.myself.frame_license_info], ba=True,b_size=1,
                                            b_color=self.primary_border_color, padding=10,
                                            background=self.color_button_pressed )
        # self.textLicense# self.textEmailAddress
        self.my_style.container_with_border([self.myself.labelEmailAddress],font_size=10, margin="0,0,5,0",
                                            ba=False, padding=5, font_color=self.color_pale_white)
        self.my_style.container_with_border([self.myself.textLicense],font_size=10, ba=False, bt=True,bb=True,
                                            padding=5, b_color=self.color_radial_gradient, b_size=3,
                                            margin="0,0,5,0", font_color=self.color_pale_white)

        # self.buttonActivateLicense
        self.my_style.button_with_border([self.myself.buttonActivateLicense], b_color=self.primary_border_color,
                                         b_radius=10, padding=5, margin="5,0",
                                         font_color=self.color_primary_black, background=self.color_primary_green)

    def _style_statistics_panel(self):

        self.my_style.container_with_border([self.myself.frame_statistics], padding=3, background=self.color_panel_bg,
                                            ba=False, bt=True, bb=True, b_size=2, b_color=self.primary_border_color)

        self.my_style.container_no_border([self.myself.labelAbout],font_color=self.primary_border_color, font_size=9)

        for child in self.myself.frame_statistics_details.children():
                # styleing only the checkbox in settings panel

                if type(child) == QPushButton:
                    self.my_style.button_no_border([child],  padding=3, font_color=self.color_pale_white,
                                                   font_size=9, margin="0,0,0,15")

                    self.my_style.append_with_hover([child], border=True, background=self.color_button_hover, b_radius=5,
                                                    b_size=1, b_color=self.primary_border_color, font_color=self.color_pale_white)
                if type(child) == QLabel:
                    self.my_style.container_with_border([child], b_size=1, b_style="solid",
                                                        b_color=self.primary_border_color, b_radius=5,
                                                        font_color=self.color_primary_green,
                                            background=self.color_panel_bg, font_size=9)

        self.my_style.button_no_border([self.myself.buttonShowHideStatistics], icon_size=20, margin=2, padding=2)

        self.my_style.append_with_hover([self.myself.buttonShowHideStatistics], border=True, b_radius=10,
                                        background=self.color_button_hover)

        self.my_style.container_with_border([self.myself.frame_resize_grip], ba=False, br=True, bb=True, b_size=1,
                                            b_color=self.primary_border_color)

    def _style_download_area_panel(self):

        self.my_style.container_no_border([self.myself.frame_downloads_list], margin="5,20")

        self.my_style.container_no_border([self.myself.parentScrolArea], padding=0, background=self.color_transparent)


class ParentItemStyleSheet():
    def __init__(self, myself, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']

    # -------------------------------------------------------------------------------
    def _set_height(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 800:
            self.myself.frame_top.setMinimumHeight(70)
            self.myself.frame_top.setMaximumHeight(80)

            self.myself.frame_refresh_playlist.setMinimumHeight(14)
            self.myself.frame_refresh_playlist.setMaximumHeight(36)
        else:
            self.myself.frame_top.setMinimumHeight(60)
            self.myself.frame_top.setMaximumHeight(60)

            self.myself.frame_refresh_playlist.setMinimumHeight(10)
            self.myself.frame_refresh_playlist.setMaximumHeight(20)

    def _get_refresh_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 20
        elif sz.height > 800 and sz.height <=960:
            return 15
        else:
            return 12

    def apply_stylesheet(self):
        self._set_height()
        self._style_centralwidget()
        self._style_top_panel(refreshIconSize=self._get_refresh_icon_size())
        self._style_parent_panel()

    # -------------------------------------------------------------------------------
    def _style_centralwidget(self):

        self.my_style.container_no_border([self.myself.centralWidget()], padding=0, background="transparent")

    def _style_top_panel(self, refreshIconSize=25):

        self.my_style.container_with_border([self.myself.frame_top], b_size=2, b_radius=20, margin="5,5,0,5",
                                            background=self.color_panel_bg, b_color=self.primary_border_color)

        self.my_style.append_with_hover([self.myself.frame_top], background=self.color_tool_bar_bg, border=True,
                                        b_color=self.color_bright_white, b_size=2, b_radius=20)

        self.my_style.button_no_border([self.myself.buttonCloseParentItem], margin=10)

        self.my_style.append_with_hover([self.myself.buttonCloseParentItem], background=self.color_button_hover,
                                        border=True, b_size=1, b_radius=8)

        self.my_style.container_with_border([self.myself.labelTitlePlaylist], padding="10,20", font_size=9,
                                            font_color=self.color_primary_green, margin="0,5,0,0", ba=False, bl=True,
                                            br=True, b_size=5, b_color=self.color_radial_gradient)

        self.my_style.container_with_border([self.myself.labelTitle], padding=0, font_size=9,
                                            font_color=self.color_primary_green, ba=False,
                                            b_color=self.color_radial_gradient, b_size=3, bl=True, br=True)

        self.my_style.label_heading_style([self.myself.labelParentStatus], padding="10,29", font_size=8,
                                          font_color=self.primary_border_color)

        labelList = [self.myself.label, self.myself.label_4, self.myself.label_2, self.myself.label_5, self.myself.label_7, self.myself.label_6, self.myself.label_3]
        self.my_style.container_with_border(labelList, padding=5, font_size=8, font_color=self.primary_border_color,
                                            ba=False, bb=True, b_size=3, b_color=self.color_radial_gradient)

        textList = [self.myself.textTotal, self.myself.textCompleted, self.myself.textDownloading, self.myself.textStopped, self.myself.textWaiting, self.myself.textError, self.myself.labelTitleTotalVideo]
        self.my_style.label_heading_style(textList, padding=5, font_size=9, font_color=self.color_primary_green)

        frameList = [self.myself.frame_status_Total, self.myself.frame_status_completed, self.myself.frame_status_downloading, self.myself.frame_stopped, self.myself.frame_waiting]
        self.my_style.container_with_border(frameList, ba=False, br=True, b_color=self.color_radial_gradient)

        self.my_style.button_no_border([self.myself.buttonShowHideDetails], margin="0,15")

        self.my_style.append_with_hover([self.myself.buttonShowHideDetails], background=self.color_button_hover,
                                        border=True, b_size=1, b_radius=7, b_color=self.primary_border_color)

        self.my_style.button_with_border([self.myself.buttonRefreshPlaylist], b_radius=8, b_size=1,
                                         b_color=self.primary_border_color, icon_size=refreshIconSize)

        self.my_style.append_with_hover([self.myself.buttonRefreshPlaylist], b_color=self.color_bright_white,
                                        background=self.color_button_hover)

        # style.container_with_border([self.frame_title], ba=False, br=True, b_size=2)
        self.my_style.container_with_border([self.myself.frame_parent_status], ba=False, bl=True, br=True, b_size=3,
                                            b_color=self.color_radial_gradient)

    def _style_parent_panel(self):

        self.my_style.container_with_border([self.myself.frame_parent], margin="-10, 20,10,100", padding=10, b_size=1,
                                            b_style="dotted", b_color=self.primary_border_color,
                                            background="rgb(40,40,40)")
        pass


class ChildItemStyleSheet():
    def __init__(self, myself, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_pale_blue = self.colorScheme['color_pale_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']

    # -------------------------------------------------------------------------------
    def _set_height(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            self.myself.frame_image.setMinimumSize(80,80)
            self.myself.frame_image.setMaximumSize(80,80)
            self.myself.setMaximumHeight(150)
        elif sz.height >= 900 and sz.height <= 960:
            self.myself.frame_image.setMinimumSize(60,60)
            self.myself.frame_image.setMaximumSize(60,60)
            self.myself.setMaximumHeight(100)
        else:
            self.myself.frame_image.setMinimumSize(60, 60)
            self.myself.frame_image.setMaximumSize(60, 60)
            self.myself.setMaximumHeight(100)

    def _get_button_radius(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 15
        elif sz.height >= 800 and sz.height <= 960:
            return 10
        else:
            return 9

    def _get_button_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 20
        elif sz.height >= 800 and sz.height <= 960:
            return 15
        else:
            return 12

    def apply_stylesheet(self):
        self._set_height()
        self._style_child(iconSize=self._get_button_icon_size(), buttonRadius=self._get_button_radius())

    # -------------------------------------------------------------------------------

    def _style_child(self, iconSize=20, buttonRadius=10):

        self.my_style.container_no_border([self.myself.centralWidget()], padding="0,0,50,0",
                                          background=self.primary_border_color)

        self.my_style.container_no_border([self.myself.frame_child],margin="0,0,3,0", padding="3",
                                          background=self.color_button_pressed)

        self.my_style.append_with_hover([self.myself.frame_child], background=self.color_pale_blue)

        self.my_style.container_no_border([self.myself.frame_title], padding=1, margin="0,0,0,40")

        self.my_style.container_no_border([self.myself.labelTitle], font_color=self.color_bright_white,
                                          font_size=10, padding=9)

        self.my_style.container_no_border([self.myself.frame_other_details], margin="0,0,0,5")

        labeList =[self.myself.label_size, self.myself.label_downloaded, self.myself.label_speed, self.myself.label_eta]
        self.my_style.container_no_border(labeList, font_color=self.color_primary_green, margin="0,5,0,0", font_size=7)

        textList = [self.myself.textSize, self.myself.textDownloaded, self.myself.textSpeed, self.myself.textETA]
        self.my_style.container_with_border(textList, font_color=self.color_bright_yellow, margin="0,20,0,0", b_size=1,
                                            b_radius=3, b_color=self.primary_border_color, font_size=8)

        self.my_style.container_no_border([self.myself.frame_progress_bar], margin="3,3")

        self.my_style.container_with_border([self.myself.progressBar], background=self.color_transparent, b_size=1,
                                            b_style="dashed", b_color=self.primary_border_color)

        self.my_style.container_with_border([self.myself.labelImage], font_color=self.primary_border_color, b_size=1,
                                            b_color=self.primary_border_color, font_size=6)

        self.my_style.container_no_border([self.myself.frame_3], padding=10)

        self.my_style.container_with_border([self.myself.frame_status], ba=False, padding=10, bl=True, b_style="dashed",
                                            b_color=self.primary_border_color, b_size=1)

        self.my_style.container_no_border([self.myself.labelStatus], font_color=self.color_bright_yellow, font_size=8)

        for child in self.myself.frame_2.children():
            if type(child) == QPushButton:
                self.my_style.button_with_border([child],margin="1,10", b_size=1, b_style="solid", icon_size=iconSize,
                                                 b_color=self.primary_border_color, padding=5, b_radius=buttonRadius)


class MessageBoxStyleSheet():
    def __init__(self, myself, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']

    # -------------------------------------------------------------------------------
    def _set_height(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            self.myself.frame_image.setMinimumSize(80,80)
            self.myself.frame_image.setMaximumSize(80,80)
            self.myself.setMaximumHeight(150)
        elif sz.height >= 900 and sz.height <= 960:
            self.myself.frame_image.setMinimumSize(60,60)
            self.myself.frame_image.setMaximumSize(60,60)
            self.myself.setMaximumHeight(100)
        else:
            self.myself.frame_image.setMinimumSize(60, 60)
            self.myself.frame_image.setMaximumSize(60, 60)
            self.myself.setMaximumHeight(100)

    def _get_button_radius(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 15
        elif sz.height >= 800 and sz.height <= 960:
            return 10
        else:
            return 9

    def _get_button_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 20
        elif sz.height >= 800 and sz.height <= 960:
            return 15
        else:
            return 12

    def apply_stylesheet(self):
        # self._set_height()
        self._style_message_box(iconSize=self._get_button_icon_size(), buttonRadius=self._get_button_radius())

    # -------------------------------------------------------------------------------

    def _style_message_box(self, iconSize=20, buttonRadius=10):

        self.my_style.container_no_border([self.myself.frame_centralwidget], padding="10",
                                          background=self.color_panel_bg)

        self.my_style.container_no_border([self.myself.frame_info_image, self.myself.frame_info],margin="3", padding="3",
                                          background=self.color_transparent)
        self.my_style.button_no_border([self.myself.buttonLogo], margin="3", padding="3",
                                       background=self.color_transparent, icon_size=50)

        self.my_style.container_no_border([self.myself.frame_info_message], background=self.color_transparent)
        self.my_style.container_no_border([self.myself.textInfo], background=self.color_transparent,
                                          font_color=self.color_primary_green, font_size=9)

        self.my_style.container_no_border([self.myself.frame], background=self.color_transparent, margin="5,0,0,0")

        self.my_style.button_with_border([self.myself.buttonYes, self.myself.buttonNo, self.myself.buttonOk],
                                       background=self.primary_border_color, font_color=self.color_pale_white,
                                       padding="3,30",b_size=1, b_color=self.color_transparent, b_radius=5)

        self.my_style.append_with_hover([self.myself.buttonYes, self.myself.buttonNo, self.myself.buttonOk],
                                        background=self.color_button_hover, font_color=self.color_bright_white)
        self.my_style.append_with_pressed([self.myself.buttonYes, self.myself.buttonNo, self.myself.buttonOk],
                                          background=self.color_button_pressed, font_color=self.color_bright_white)

        # self.my_style.append_with_hover([self.myself.frame_child], background=self.color_bright_blue)


class RegisterDialogStyleSheet():
    def __init__(self, myself, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']

    # -------------------------------------------------------------------------------
    def _set_height(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 900:
            self.myself.frame_image.setMinimumSize(80,80)
            self.myself.frame_image.setMaximumSize(80,80)
            self.myself.setMaximumHeight(150)
        elif sz.height >= 900 and sz.height <= 960:
            self.myself.frame_image.setMinimumSize(60,60)
            self.myself.frame_image.setMaximumSize(60,60)
            self.myself.setMaximumHeight(100)
        else:
            self.myself.frame_image.setMinimumSize(60, 60)
            self.myself.frame_image.setMaximumSize(60, 60)
            self.myself.setMaximumHeight(100)

    def _get_button_radius(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 15
        elif sz.height >= 800 and sz.height <= 960:
            return 10
        else:
            return 9

    def _get_button_icon_size(self):
        sz = GeneralFunctions().get_screen_size()
        if sz.height > 960:
            return 20
        elif sz.height >= 800 and sz.height <= 960:
            return 15
        else:
            return 12

    def apply_stylesheet(self):
        # self._set_height()
        self._style_registration_dialog(iconSize=self._get_button_icon_size(), buttonRadius=self._get_button_radius())

    # -------------------------------------------------------------------------------

    def _style_registration_dialog(self, iconSize=20, buttonRadius=10):

        self.my_style.container_no_border([self.myself.frame_centralwidget], padding="5,10",
                                          background=self.color_panel_bg)

        self.my_style.container_no_border([self.myself.frame, self.myself.frame_2, self.myself.frame_3],
                                          padding="5",background=self.color_transparent)

        self.my_style.container_no_border([ self.myself.frame_4],background=self.color_transparent)

        self.my_style.container_no_border([self.myself.labelInfo],font_color=self.color_primary_green,
                                          font_size=9, background=self.color_transparent)

        self.my_style.container_no_border([self.myself.label_2, self.myself.label_3, self.myself.label_4],
                                          font_color=self.color_primary_green,padding="3",
                                          font_size=8, background=self.color_transparent)

        self.my_style.button_with_border([self.myself.buttonRegister, self.myself.buttonCancel],
                                         background=self.primary_border_color, font_color=self.color_pale_white,
                                         padding="3,30", b_size=1, b_color=self.color_transparent, b_radius=5)

        self.my_style.button_with_border([self.myself.buttonShowHidePassword],
                                         background=self.primary_border_color, font_color=self.color_pale_white,
                                         padding="3", b_size=1, b_color=self.color_transparent, b_radius=5)

        self.my_style.append_with_hover([self.myself.buttonShowHidePassword,self.myself.buttonRegister, self.myself.buttonCancel],
                                        background=self.color_button_hover, font_color=self.color_bright_white)

        self.my_style.append_with_pressed([self.myself.buttonShowHidePassword, self.myself.buttonRegister, self.myself.buttonCancel],
                                          background=self.color_button_pressed, font_color=self.color_bright_white)

        self.my_style.container_with_border([self.myself.textUsername, self.myself.textEmail, self.myself.textPassword], padding="3",
                                            background=self.color_pale_white, b_radius=5, font_size=8,
                                            font_color=self.color_primary_black)
        self.my_style.container_with_border([self.myself.labelWarningMessage], ba=False, bt=True, bb=True, b_size=1,
                                            b_color=self.primary_border_color, margin="5,0", font_size=8,
                                            font_color="red", padding="5,0")


class MenuItemStyleSheet():

    def __init__(self, color_scheme=ColorScheme().dark_theme()):
        self.my_style = JbadonaiStyleSheetCode()
        # self.myself = myself
        self.colorScheme = color_scheme
        self.color_radial_gradient = self.colorScheme['color_radial_gradient']
        self.color_primary_green = self.colorScheme['color_primary_green']
        self.color_primary_black = self.colorScheme['color_primary_black']
        self.color_pale_white = self.colorScheme['color_pale_white']
        self.primary_border_color = self.colorScheme['primary_border_color']
        self.color_transparent = self.colorScheme['color_transparent']
        self.color_bright_yellow = self.colorScheme['color_bright_yellow']
        self.color_bright_white = self.colorScheme['color_bright_white']
        self.color_bright_blue = self.colorScheme['color_bright_blue']
        self.color_bright_red = self.colorScheme['color_bright_red']

        self.color_title_bar_bg = self.colorScheme['color_title_bar_bg']
        self.color_tool_bar_bg = self.colorScheme['color_tool_bar_bg']
        self.color_central = self.colorScheme['color_central']
        self.color_button_hover = self.colorScheme['color_button_hover']
        self.color_button_pressed = self.colorScheme['color_button_pressed']
        self.color_panel_bg = self.colorScheme['color_panel_bg']
        self.color_bright_hover = self.colorScheme['color_bright_hover']


    def context_menu_stylesheet(self):
        style = """
            QMenu{
               color: rgb(0, 255, 127);
               background-color: rgb(10, 10, 10);
               border-left: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-right: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-top: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               border-bottom: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
               margin-left:2px;
               padding-left:10px;
               font:9pt;
            }

           QMenu::item::selected{
               color: white;
               background-color: blue;
               font:9pt;
               padding-left:13px;
           }

           QMenu::separator{
            background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
           }

        """
        return style
