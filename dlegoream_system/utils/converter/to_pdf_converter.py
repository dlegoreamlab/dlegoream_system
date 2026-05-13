from weasyprint import HTML


class PdfConverter:

    def html_to_pdf(self, html: str, output_path: str):

        HTML(string=html).write_pdf(output_path)

        return output_path