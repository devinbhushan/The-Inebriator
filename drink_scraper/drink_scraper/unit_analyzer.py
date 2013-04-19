class Unit_Analyzer():

    def __init__(self):
        self.unit_filters = ["oz", "dash", "tsp", "tbsp", "pony", "jigger", "cup",
                             "pt", "qt", "gal", "splash", "dash", "float", "part",
                             "tablespoon", "teaspoon", "ponies", "gallon", "quart",
                             "ounce"]

    def get_triple(self, input_text):
        """
        Given a string in the form "[quantity][A-Z, 0-9]*[unit][A-Z, 0-9]*[ingredient]"
        Returns triple of form (quantity, unit, ingredient)
        """
        #find units
        words = input_text.split()
        unit_selected = None
        for curr_unit in self.unit_filters:
            extensions = ["", ".", "s", "es"]
            for extension in extensions:
                expanded_unit = "%s%s" % (curr_unit, extension)
                if expanded_unit in words:
                    unit_selected = expanded_unit
                    break

        # In case no units exist
        if unit_selected is None:
            return (None, input_text, None)

        quantity, ingredient = input_text.split(unit_selected)
        #print "quantity:%s, ingredient:%s, unit:%s" % (quantity.strip(), ingredient.strip(), unit_selected.strip())
        return (quantity.strip(), ingredient.strip(), unit_selected.strip())


def main():
    """
    Tests get_triple
    """
    unit_analyzer = Unit_Analyzer()
    unit_analyzer.get_triple("1 oz vodka")
    unit_analyzer.get_triple("1 tsps vodka")

if __name__ == "__main__":
    main()
