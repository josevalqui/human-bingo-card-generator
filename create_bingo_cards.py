import pandas as pd
import random
from weasyprint import HTML
from PyPDF2 import PdfMerger
import io

# load spreadsheet
xl = pd.ExcelFile('prompts.xlsx')

# load a sheet into a DataFrame
df = xl.parse('Sheet1')

def generate_unique_prompts(df, num_cards):
    df_1 = df[df['Difficulty']==1].sample(frac=1).reset_index(drop=True)  # shuffle prompts
    df_2 = df[df['Difficulty']==2].sample(frac=1).reset_index(drop=True)
    df_3 = df[df['Difficulty']==3].sample(frac=1).reset_index(drop=True)

    prompts_per_card = [10, 10, 5]
    df_list = [df_1, df_2, df_3]
    
    card_prompts = []
    
    for i in range(num_cards):
        prompts = []
        for j in range(3):  # for each difficulty level
            start_index = (i * prompts_per_card[j]) % len(df_list[j])
            end_index = start_index + prompts_per_card[j]
            
            if end_index <= len(df_list[j]):
                prompts.extend(df_list[j].iloc[start_index:end_index]['Prompt'].tolist())
            else:
                # wrap around to the beginning if we run out of unique prompts
                prompts.extend(df_list[j].iloc[start_index:]['Prompt'].tolist())
                prompts.extend(df_list[j].iloc[:end_index-len(df_list[j])]['Prompt'].tolist())
                
                # reshuffle the prompts for this difficulty level
                df_list[j] = df_list[j].sample(frac=1).reset_index(drop=True)
        
        card_prompts.append(prompts)
    
    return card_prompts

def create_html_card(prompts, card_number):
    random.shuffle(prompts)  # Shuffle the prompts
    matrix = [prompts[n:n+5] for n in range(0, len(prompts), 5)]

    # Create HTML content
    html_content = f"""
    <div class="card">
    <table>
    """
    for row in matrix:
        html_content += "<tr>"
        for cell in row:
            html_content += f"<td>{cell}</td>"
        html_content += "</tr>"
    html_content += """
    </table>
    </div>
    """
    return html_content

def create_bingo_cards(df, start_card_number, end_card_number):
    unique_prompts = generate_unique_prompts(df, end_card_number - start_card_number + 1)
    
    html_cards = []
    for i, card_number in enumerate(range(start_card_number, end_card_number+1)):
        html_cards.append(create_html_card(unique_prompts[i], card_number))

    # Wrap cards in HTML and CSS
    html_content = f"""
    <html>
    <head>
    <style>
    @page {{
        margin-top: 0.5cm;
        margin-bottom: 0.5cm;
        margin-left: 0.5cm;
        margin-right: 0.5cm;
    }}
    body {{
      display: block;
      width: 100%;
      margin: 0;
      padding: 0;
    }}
    .card {{
      display: block;
      width: calc(100% - 20px);
      margin: auto;
      margin-bottom: 60px;
      padding: 20px;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      table-layout: fixed;
    }}
    th, td {{
      border: 1px solid black;
      text-align: center;
      padding: 15px;
      word-wrap: break-word;
    }}
    </style>
    </head>
    <body>
    {"".join(html_cards)}
    </body>
    </html>
    """

    # Convert HTML to PDF
    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return pdf_io

# Create pairs of bingo cards as an example
pdfs = []
for i in range(0, 30, 2):
    pdfs.append(create_bingo_cards(df, i+1, i+2))

# Merge PDFs
merger = PdfMerger()
for pdf in pdfs:
    merger.append(pdf)

# Save combined PDF
with open("Combined_Bingo_Cards.pdf", "wb") as f_out:
    merger.write(f_out)

merger.close()
