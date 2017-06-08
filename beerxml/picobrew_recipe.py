from pybeerxml.recipe import Recipe
import hashlib


class PicoBrewRecipe(Recipe):

    def __init__(self, parent):
        super(Recipe, self).__init__()
        self.__dict__ = parent.__dict__

        # create a unique id for every recipe based on the filename
        hasher = hashlib.md5()
        print(self.filename)
        encoded_filename = self.filename.encode('utf-8')
        hasher.update(encoded_filename)
        self.id = hasher.hexdigest()[:32]
        self.steps = []


    def serialize(self):
        return "{0}/{1}/{2}/".format(
            self.name,
            self.id,
            self.get_recipe_steps(),
        )

    def get_recipe_steps(self):
        steps = [step.serialize() for step in self.steps]
        print(steps)
        return "/".join(steps)

    def save(self):
        pass
