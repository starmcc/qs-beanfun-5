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

        QMenu {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 2px 0;
            font-size: 12px;
        }

        QMenu::item {
            padding: 4px 20px 4px 12px;
            margin: 1px 0;
            color: #333333;
        }

        QMenu::item:selected {
            background-color: #e6f2ff;
            color: #0052cc;
        }

        QMenu::separator {
            height: 1px;
            background-color: #eeeeee;
            margin: 2px 4px;
        }

        /* 新增按钮基础+移入浅蓝效果，匹配你菜单浅蓝色 #e6f2ff */
        QPushButton {
            color: #333333;
        }
        QPushButton:hover {
            background-color: #e6f2ff;
            color: #0052cc;
        }
    """

    TRAY_MENU_STYLE = """
        QMenu {
            background-color: #2D3748;
            border: 1px solid #4A5568;
            border-radius: 8px;
            padding: 6px;
            color: #E2E8F0;
            font-family: 'Microsoft YaHei', sans-serif;
            font-size: 12px;
        }
        QMenu::item {
            padding: 8px 16px;
            border-radius: 4px;
            margin: 2px;
        }
        QMenu::item:selected {
            background-color: #4299e1;
            color: white;
        }
        QMenu::separator {
            height: 1px;
            background-color: #4A5568;
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