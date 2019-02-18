

class Chart(object):
    """
    Main Object for django simple charts
    """
    columns = []
    data_dictionary = None
    x_label = 'X'
    y_label = 'Y'
    axis = True
    x_step = None
    y_step = None
    x_number_step = None
    y_number_step = None
    min_x = None
    max_x = None
    min_y = None
    max_y = None

    def __init__(self):
        pass

    def set_columns(self, columns):
        self.columns = columns

    def set_x_label(self, x_label):
        self.x_label = x_label
        return self

    def set_y_label(self, y_label):
        self.y_label = y_label
        return self

    def set_axis(self, axis):
        self.axis = bool(axis)
        return self

    def set_x_step(self, x_step):
        self.x_step = x_step
        return self

    def set_y_step(self, y_step):
        self.y_step = y_step
        return self

    def set_x_number_step(self, x_number_step):
        self.x_number_step = x_number_step
        return self

    def set_y_number_step(self, y_number_step):
        self.y_number_step = y_number_step
        return self

    def set_min_x(self, min_x):
        self.min_x = min_x
        return self

    def set_max_x(self, max_x):
        self.max_x = max_x
        return self

    def set_min_y(self, min_y):
        self.min_y = min_y
        return self

    def set_max_y(self, max_y):
        self.max_y = max_y
        return self

    @staticmethod
    def _check_has_attr(obj, attr_list):
        """
        Check if an object has all of the attrs item
        :param obj:
        :param attr_list:
        :return:
        """
        return all([hasattr(obj, x) for x in attr_list])

    @staticmethod
    def _cast_to_float(obj):
        """
        Cast an object to float or return None
        :param obj:
        :return:
        """
        try:
            return float(obj)
        except ValueError:
            return None
