class DocumentRenderer:

    def render(self, doc: dict, images: list):

        html = f"""
        <html>
        <head>
        <meta charset="utf-8">

        <style>

        body {{
            font-family: Arial;
            margin: 40px;
            line-height: 1.7;
        }}

        h1 {{
            border-bottom: 2px solid black;
            padding-bottom: 10px;
        }}

        h2 {{
            margin-top: 30px;
            border-left: 4px solid black;
            padding-left: 10px;
        }}

        img {{
            width: 100%;
            margin: 20px 0;
        }}

        </style>

        </head>
        <body>

        <h1>{doc['title']}</h1>

        <p>{doc['summary']}</p>
        """

        img_index = 0

        for sec in doc["sections"]:

            html += f"""
            <h2>{sec['title']}</h2>
            <p>{sec['text']}</p>
            """

            # 이미지 삽입 (순서대로)
            if img_index < len(images):

                html += f"""
                <img src="{images[img_index]}">
                """

                img_index += 1

        html += """
        </body>
        </html>
        """

        return html