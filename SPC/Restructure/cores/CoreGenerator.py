from SPC.Restructure.UIO import UIO

class CoreGenerator:

    def generateCore(self, seq):
        """
        abstract function
        """
        pass

    def compareTwoCoreElements(self, a, b):
        """
        abstract function
        """
        pass

    @staticmethod
    def getCoreComparisions(partition):
        """
        abstract function
        """
        pass

    @staticmethod
    def getCoreLabels(partition):
        """
        abstract function
        """
        pass

    def __init__(self, uio:UIO, partition):
        self.uio = uio
        self.partition = partition

        # this attribute is common for all coregenerator even when they have different UIO. So it should be a class attribute
        if not hasattr(self, "comp_indices"):
            comp_indices = []

            labels = self.getCoreLabels(partition)
            comp = self.getCoreComparisions(partition)

            for first_index, first_label in enumerate(labels):
                if first_label in comp:
                    for second_label in comp[first_label]:
                        second_index = labels.index(second_label)
                        comp_indices.append((first_index, second_index))

            # Set the calculated comp_indices for all CoreGenerators of this type (but not the base class)
            type(self).comp_indices = comp_indices
            print("Reduced size of core representations: {} -> {}".format(len(labels)*(len(labels)-1)/2, len(comp_indices)))

    def getCoreRepresentation(self, core):
        if core == "GOOD":
            return "GOOD"

        if core == "BAD":
            return "BAD"
        
        return tuple([self.compareTwoCoreElements(core[f_index], core[s_index]) for f_index, s_index in self.comp_indices])
    
    @classmethod
    def getCoreRepresentationLength(cls, partition):
        labels = cls.getCoreLabels(partition)
        comp = cls.getCoreComparisions(partition)
        return sum([len(comp[label]) for label in labels if label in comp])
    
    @classmethod
    def getCoreLength(cls, partition):
        return len(cls.getCoreLabels(partition))
    
    @classmethod
    def getAllCoreComparisions(cls, partition):
        comp = {}
        labels = cls.getCoreLabels(partition)
        for index,label in enumerate(labels):
            comp[label] = labels[index+1:]
        return comp


    