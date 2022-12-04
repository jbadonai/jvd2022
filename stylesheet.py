
# class Stylesheet():
#     def __init__(self):
#         super(Stylesheet, self).__init__()
#
#         self.parentItemDarkTheme = """
#         #centralwidget{
#         padding: 0px;
#         background: transparent;
#         }
#
#         #frame_top{
#         border:2px solid gray;
#         border-radius:20px;
#         margin: 5px 5px 0px 5px;
#         background-color: rgb(20,20,20);
#         }
#
#         #frame_top:hover{
#         border:2px solid white;
#         border-radius:20px;
#         margin: 5px 5px 0px 5px;
#         background-color: rgb(15,15,15);
#         }
#
#         #buttonCloseParentItem{
#         margin: 10px;
#
#         }
#
#         #buttonCloseParentItem:hover{
#         background-color: rgb(45,45,45);
#         border: 1px solid gray;
#         border-radius: 8px;
#
#         }
#
#         #labelTitlePlaylist{
#         padding: 10px 20px;
#         font-size: 10pt;
#         color: rgb(0, 255, 127);
#         margin-right: 5px;
#         border-left:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#         border-right:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#         }
#
#         #label_3{
#         border-bottom:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#         padding-bottom: 5px;
#         }
#
#         #labelTitleTotalVideo{
#         padding: 5px;
#         font-size: 10pt;
#         color: rgb(0, 255, 127);
#         }
#
#
#         #labelTitle {
#         padding: 0;
#         font-size: 12pt;
#         color: rgb(0, 255, 127);
#         border-left:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#         }
#
#
#         #labelParentStatus{
#         padding: 10px 20px;
#         font-size: 8pt;
#         color: gray;
#         }
#
#         #label, #label_4, #label_2, #label_5, #label_7, #label_6{
#         padding: 5px;
#         font-size: 8pt;
#         color: gray;
#         border-bottom:3px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#
#         }
#
#
#         #textTotal, #textCompleted, #textDownloading, #textStopped, #textWaiting, #textError{
#         padding: 5px;
#         font-size: 9pt;
#         color: rgb(0, 255, 127);
#         }
#
#         #frame_parent_status:hover{
#         color: yellow;
#
#         }
#
#         #frame_status_Total, #frame_status_completed, #frame_status_downloading, #frame_stopped, #frame_waiting {
#         border-right:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#
#         }
#
#                  #buttonShowHideDetails{
#          margin-left:15px;
#          margin-right:15px;
#          }
#
#         #buttonShowHideDetails:hover{
#         background-color: rgb(45,45,45);
#         border: 1px solid gray;
#         border-radius: 8px;
#         }
#
#                 #frame_refresh_playlist QPushButton{
#         background-color: rgb(45,45,45);
#         border: 1px solid gray;
#         border-radius: 8px;
#
#                #frame_title{
#             border-right:2px solid gray;
#         }
#
#
#         #frame_parent_status{
#         border-left:2px solid gray;
#         border-right:5px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#
#         }
#
#
#         #frame_parent{
#         margin: -10px 20px 10px 100px;
#         padding:10px;
#         border-radius: 10px;
#         border: 1px dotted gray;
#         background-color: rgb(40,40,40);
#         }
#
#
#
#         #frame_refresh_playlist{
#         }
#
#
#
#
#         """
#
#         self.childItemDarkTheme = """
#         #centralwidget{
#         padding-bottom:50px;
#         background-color:gray;
#         }
#
#
#         #frame_child{
#         margin-bottom: 3px;
#         padding-bottom: 3px;
#         background-color:rgb(35,35,35);
#         }
#
#         #frame_child:hover{
#         border-right:10px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#         margin-bottom: 3px;
#         background-color: rgb(25,25,25);
#         }
#
#         #frame_title{
#         padding:1px;
#
#         margin-left:40px;
#         }
#
#         #labelTitle{
#         color: white;
#         font: 10pt;
#         padding:0px;
#         }
#
#         #frame_other_details{
#         margin-left:5px;
#         }
#
#         #label_size, #label_downloaded, #label_speed, #label_eta{
#         color: rgb(0, 255, 127);
#         margin-right: 5px;
#         }
#
#         #textSize, #textDownloaded, #textSpeed, #textETA{
#         color: yellow;
#         margin-right:20px;
#         border:1px solid gray;
#         border-radius: 3px;
#         }
#
#         #frame_stats{
#         }
#
#         #frame_progress_bar{
#         margin: 3px, 3px;
#
#         }
#
#         #progressBar{
#         background-color:transparent;
#         border:1px dotted gray;
#
#         }
#
#         #frame_image QLabel{
#         color: gray;
#         border: 1px solid gray;
#         }
#
#
#         #frame_3{
#         padding:10px;
#         }
#
#         #frame_status {
#         border-left:1px dashed gray;
#         padding-left: 10px;
#         }
#
#
#         #labelStatus{
#         color: yellow;
#         font-size: 8pt;
#         }
#
#
#         #labelStandardStatus{
#         background-color: transparent;
#         color: gray;
#         border-bottom: yellow;
#         font-size:6pt;
#         }
#
#
#         #frame_status QPushButton{
#         margin: 5px 15px;
#         border: 1px solid gray;
#         padding: 5px;
#         border-radius: 15px;
#
#         }
#
#
#
#         """
#
#         self.menuDarkTheme = """
#
#                QMenu{
#                color: rgb(0, 255, 127);
#                background-color: rgb(10, 10, 10);
#                border-left: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#                border-right: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#                border-top: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#                border-bottom: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#                margin-left:2px;
#                padding-left:10px;
#                font:9pt;
#
#                }
#
#
#                QMenu::item::selected{
#                color: white;
#                background-color: blue;
#                font:9pt;
#                /*font-style: italic;*/
#                padding-left:13px;
#                }
#
#                QMenu::separator{
#                background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));
#
#                }
#
#
#                """
#

class TextColor():
    def __init__(self):
        self.waiting_color = "rgb(240, 217, 219)"
        self.stopped_color = "rgb(181, 207, 237)"
        self.downloading_color = "yellow"
        self.completed_color = "rgb(0,255,127)"
