class StyleConstants:
    GLOBAL_STYLE = """
        * {
            font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
        }

        QLineEdit {
            border: 1px solid #a0a0a0;
            border-radius: 3px;
            padding-left: 5px;
            background-color: transparent;
            color: black;
            selection-background-color: #F57C00;
            font-size: 10pt;
        }

        QLineEdit:hover {
            border: 1px solid #F57C00;
            border-radius: 3px;
            background-color: #f2f2f2;
            color: #F57C00;
            selection-background-color: #F57C00;
        }

        QLineEdit[echoMode="2"] {
            lineedit-password-character: 9679;
        }

        QPushButton {
            color: #333333;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            margin: 2px 2px;
            padding: 3px 10px;
            min-height: 22px;
        }
        QPushButton:hover {
            background-color: #e6f2ff;
            color: #0052cc;
        }
    """
    TITLE_BTN = """
        QPushButton {
            color: white;
            border: 0;
            border-radius: 6px;
            background-color: transparent;
            padding: 3px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.11);
        }
    """

    MENU_STYLE = """
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 4px 0;
            /* 轻微阴影，脱离桌面层级，更立体 */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }
        
        QMenu::item {
            padding: 6px 22px 6px 14px;
            margin: 0 4px;
            border-radius: 4px;
            color: #2c333a;
            font-size: 12px;
        }
        
        QMenu::item:selected {
            background-color: #eff7ff;
            color: #1967d2;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #f0f0f0;
            margin: 4px 8px;
        }
    """

    TIPS_WIN_STYLE = """
    background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    """