import re
import json
import pymupdf # pip install PyMuPDF

class GetRecipesFromPDF:
    def __init__(self, pdf_file_path, pages_numbers_list):
        """Get content from PDF file"""
        self.pdf_file_path = pdf_file_path

        doc = pymupdf.open(pdf_file_path)
        self.title_list = []
        self.ingredients_list = []
        self.servings_list = []
        self.description_list = []
        self.time_list = []

        if pages_numbers_list:
            for page_number in pages_numbers_list:
                self.description_list.append(f'Recipe from the page {page_number} from "Wysokobiałkowy wegański '
                                             f'jadłospis DIY" by Irena Owsiak')
                page = doc[page_number-1]
                self.extract_info_from_page(page)
        doc.close()

    def extract_info_from_page(self, page):
        # TODO: get recipe instructions
        servings_start = 'Składniki na:'
        servings_end = 'porcj'
        time_start = 'Zrobisz w:'
        time_end = 'minut'
        text = page.get_text().strip().replace(" ", "")  # get plain text encoded as UTF-8
        if text:
            ingredients = self.get_recipe_ingredients(text)
            if ingredients:
                self.ingredients_list.append(ingredients)
                self.title_list.append(self.get_recipe_title(text))
                self.servings_list.append((text.split(servings_start))[1].split(servings_end)[0].strip())
                self.time_list.append((text.split(time_start))[1].split(time_end)[0].strip())

    @staticmethod
    def get_recipe_ingredients(text):
        text_lines = text.split("\n")
        is_an_ingredient = [True if "•" in line else False for line in text_lines]
        # Finding the line of a recipe without "•" character - on the (i+1) index
        for i in range(0, len(text_lines)-2):
            if is_an_ingredient[i] and not is_an_ingredient[i+1] and is_an_ingredient[i+2]:
                text_lines[i] = text_lines[i].strip()+" "+text_lines[i+1].strip()
        recipe_text_lines = [line.strip().replace("•	 ", "• ").replace("•	", "• ")
                             for line in text_lines if "•" in line]
        recipe = ("\n").join(recipe_text_lines).strip()
        return recipe

    @staticmethod
    def get_recipe_title(text):
        with open("../env/polish_short_words.json", "r", encoding="utf") as f:
            polish_short_words = json.load(f)
        upper_case_words = re.findall(r'\b[A-ZĄĆĘŁŃÓŚŹŻ]+\b', text)
        ok_words = [w for w in upper_case_words if (len(w)>2 or w.lower() in polish_short_words)]
        return (" ".join(ok_words)
                .replace("PRZYGOTOWANIE", "")
                .replace("SKŁADNIKI", "")
                .replace("KLIK", "")
                .replace("\n", " ")
                .strip()
                )

    def correct_titles_user_input(self):
        for i, title in enumerate(self.title_list):
            input_title = input(f"Current title: {title}\nIs that proper recipe title? "
                                       f"If yes click ENTER, if not, enter new title: ")
            if input_title:
                self.title_list[i] = input_title



if __name__ == "__main__":
    recipe_pdf = GetRecipesFromPDF("../test/2000-kcal-DIY-WYSOKOBIALKOWY.pdf",
                                   [75, 95, 102, 111, 118, 136, 138, 140])
    recipe_pdf.correct_titles_user_input()

    # test
    print(recipe_pdf.title_list)
    # print(recipe_pdf.ingredients_list)
    print(recipe_pdf.servings_list)
    print(recipe_pdf.description_list)
    print(recipe_pdf.time_list)

