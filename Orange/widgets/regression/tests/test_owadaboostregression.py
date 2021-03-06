# Test methods with long descriptive names can omit docstrings
# pylint: disable=missing-docstring
from Orange.regression import (
    SklTreeRegressionLearner,
    KNNRegressionLearner,
    RandomForestRegressionLearner
)
from Orange.widgets.regression.owadaboostregression import OWAdaBoostRegression
from Orange.widgets.tests.base import (
    WidgetTest, WidgetLearnerTestMixin, ParameterMapping
)


class TestOWAdaBoostRegression(WidgetTest, WidgetLearnerTestMixin):
    def setUp(self):
        self.widget = self.create_widget(OWAdaBoostRegression,
                                         stored_settings={"auto_apply": False})
        self.init()
        losses = [loss.lower() for loss in self.widget.losses]
        self.parameters = [
            ParameterMapping('loss', self.widget.loss_combo, losses),
            ParameterMapping('learning_rate', self.widget.learning_rate_spin),
            ParameterMapping('n_estimators', self.widget.n_estimators_spin)]

    def test_input_learner(self):
        """Check if base learner properly changes with learner on the input"""
        max_depth = 2
        default_base_est = self.widget.base_estimator
        self.assertIsInstance(default_base_est, SklTreeRegressionLearner)
        self.assertIsNone(default_base_est.params.get("max_depth"))
        self.send_signal("Learner",
                         SklTreeRegressionLearner(max_depth=max_depth))
        self.assertEqual(self.widget.base_estimator.params.get("max_depth"),
                         max_depth)
        self.widget.apply_button.button.click()
        output_base_est = self.get_output("Learner").params.get("base_estimator")
        self.assertEqual(output_base_est.max_depth, max_depth)

    def test_input_learner_that_does_not_support_sample_weights(self):
        self.send_signal("Learner", KNNRegressionLearner())
        self.assertNotIsInstance(
            self.widget.base_estimator, KNNRegressionLearner)
        self.assertIsNone(self.widget.base_estimator)
        self.assertTrue(self.widget.Error.no_weight_support.is_shown())

    def test_error_message_cleared_when_valid_learner_on_input(self):
        # Disconnecting an invalid learner should use the default one and hide
        # the error
        self.send_signal("Learner", KNNRegressionLearner())
        self.send_signal('Learner', None)
        self.assertFalse(
            self.widget.Error.no_weight_support.is_shown(),
            'Error message was not hidden on input disconnect')
        # Connecting a valid learner should also reset the error message
        self.send_signal("Learner", KNNRegressionLearner())
        self.send_signal('Learner', RandomForestRegressionLearner())
        self.assertFalse(
            self.widget.Error.no_weight_support.is_shown(),
            'Error message was not hidden when a valid learner appeared on '
            'input')

    def test_input_learner_disconnect(self):
        """Check base learner after disconnecting learner on the input"""
        self.send_signal("Learner", RandomForestRegressionLearner())
        self.assertIsInstance(
            self.widget.base_estimator, RandomForestRegressionLearner)
        self.send_signal("Learner", None)
        self.assertEqual(self.widget.base_estimator,
                         self.widget.DEFAULT_BASE_ESTIMATOR)
