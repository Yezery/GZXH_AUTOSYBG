from qfluentwidgets import InfoBar,InfoBarPosition

from PyQt6.QtCore import Qt

def createMessage(parent=None,title="",message="",_type=3):
        match _type:
            case 0:
                InfoBar.error(
                    title=title,
                    content=message,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            case 1:
                InfoBar.success(
                    title=title,
                    content=message,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            case 2:
                InfoBar.warning(
                    title=title,
                    content=message,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            case 3:
                InfoBar.info(
                    title=title,
                    content=message,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
