"""Widget for induction of regression trees"""

from Orange.modelling.tree import TreeLearner
from Orange.widgets.model.owtree import OWTreeLearner
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner


class OWTreeLearner(OWTreeLearner):
    name = "Regression Tree"
    description = "A regression tree algorithm with forward pruning."
    icon = "icons/RegressionTree.svg"
    priority = 30

    LEARNER = TreeLearner

    # Disable the special classification layout to be used when widgets are
    # fully merged
    add_classification_layout = OWBaseLearner.add_classification_layout


def _test():
    import sys
    from AnyQt.QtWidgets import QApplication
    from Orange.data import Table

    a = QApplication(sys.argv)
    ow = OWRegressionTree()
    d = Table('housing')
    ow.set_data(d)
    ow.show()
    a.exec_()
    ow.saveSettings()

if __name__ == "__main__":
    _test()
