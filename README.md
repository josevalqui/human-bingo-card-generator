# Human Bingo Card Generator
A Python script that takes an Excel file of prompts with corresponding difficulty levels (1-3) and generates a PDF with unique and (difficulty-) balanced Human Bingo cards.


Prerequisites

    Python 3.x
    Libraries: pandas, weasyprint, PyPDF2
    prompts.xlsx file with prompts and their corresponding difficulty level (1-3)

Editable variables

  prompts_per_card: number of prompts from each difficulty level in each card (has to add up to 25)
  num_cards: number of cards that should be generated

Output

  The script will generate a PDF file (x_Bingo_Cards.pdf') with two bingo cards per page.

Things to look out for

  The prompts should be no longer than around 30 characters (5-6 words)


  
