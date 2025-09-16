class StyleConstants:
    # 全局样式
    GLOBAL_STYLE = """
        * {
        font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
        }

        QLineEdit {
        border: 1px solid #a0a0a0;  /* 边框宽度为 1px，颜色为 #a0a0a0 */
        border-radius: 3px;  /* 边框圆角 */
        padding-left: 5px;  /* 文本距离左边界有 5px */
        background-color: transparent;  /* 背景颜色 */
        color: black;  /* 文本颜色 */
        selection-background-color: #F57C00;  /* 选中文本的背景颜色 */
        font-size: 10pt;  /* 文本字体大小 */
        }

        QLineEdit:hover {  /* 鼠标悬浮在 QLineEdit 时的状态 */
            border: 1px solid #F57C00;
            border-radius: 3px;
            background-color: #f2f2f2;
            color: #F57C00;
            selection-background-color: #F57C00;
        }

        QLineEdit[echoMode="2"] {  /* QLineEdit 有输入掩码时的状态 */
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
            padding: 4px 20px 4px 12px; /* 上下4px，左右12/20（右侧给快捷键留空间） */
            margin: 1px 0;
            color: #333333;
        }
        
        QMenu::item:selected {
            background-color: #e6f2ff; /* 选中时浅蓝背景 */
            color: #0052cc;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #eeeeee;
            margin: 2px 4px;
        }
        
        """
