class MashStep(object):
    def __init__(self):
        self.name = None
        self.version = None
        self.type = None
        self.infuse_amount = None
        self.step_temp = None
        self.step_time = None
        self.ramp_time = None
        self.end_temp = None

        @property
        def waterRatio(self):
            raise NotImplementedError("waterRation")
            # water_amout = self.infuse_amount or self.decoction_amt
            # return water_amount / recipe.grainWeight()