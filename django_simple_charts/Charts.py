import math

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


class QuantitativeChart(Chart):

    @staticmethod
    def _try_get_nested_value_from_dictionary(dictionary, *ordered_keys):
        """
        Get nested key from dictionary or return none
        :param dictionary:
        :param args: ordered keys
        :return:
        """
        if ordered_keys:
            value = dictionary
            try:
                for key in ordered_keys:
                    value = value[key]
            except KeyError:
                value = None
            return value

    def complete_quantitative_attrs(self):
        """
        Complete Attributes with None Value to default based queryset selected columns.
        :return: self histogram object
        """
        if self.data_dictionary:
            x_min_list = [min(self._try_get_nested_value_from_dictionary(self.data_dictionary, x, 'data')) for x in
                          self.columns]
            if not self.min_x:
                self.min_x = min(x_min_list)
            x_max_list = [max(self._try_get_nested_value_from_dictionary(self.data_dictionary, x, 'data')) for x in
                          self.columns]
            if not self.max_x:
                self.max_x = max(x_max_list)


class Histogram(QuantitativeChart):
    """
    Histogram object, style, range and plot
    """
    queryset = None
    breaks = None
    bins_width = None
    _histogram_dictionary = dict()

    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_quantile(data, r):
        """
        Get Quantile for r proportion (ie. 0.25 for Q1 and 0.5 for median)
        :param data:
        :param r:
        :return:
        """
        if data:
            size = data.__len__()
            return data[math.floor(size * r)]

    def _get_interquartile_range(self, data):
        """
        Get Interquantile Range (Q3 - Q1)
        :param data:
        :return:
        """
        if data:
            return self._get_quantile(data, 0.75) - self._get_quantile(data, 0.25)

    def _get_default_histogram_width(self, data):
        """
        Get Default histogram withs
        :param data:
        :return:
        """
        if data:
            return 2 * self._get_interquartile_range(data) / (data.__len__() ** (1 / 3))

    def _get_aggregated_data(self):
        """
        Aggregate all columns data in one list
        :return:
        """
        if self.data_dictionary:
            raw_list = [self._try_get_nested_value_from_dictionary(self.data_dictionary, x, 'data') for x in
                        self.columns]
            return [y for x in raw_list for y in x]

    @staticmethod
    def _count_data_in_range(data, min, max):
        """
        Count Number of data on a specific range for a list
        :param data:
        :param min:
        :param max:
        :return:
        """
        return [x for x in data if min <= x < max].__len__()

    def _get_histogram_dictionary_for_column(self, column):
        """
        Get list of dictionaries (one list for each bin)
        :param column:
        :return:
        """
        histogram_column = list()
        data = self._try_get_nested_value_from_dictionary(self.data_dictionary, column, 'data')
        if data:
            for bin_index in range(self.breaks):
                min_bin = self.min_x + bin_index * self.bins_width
                max_bin = min_bin + self.bins_width
                histogram_column.append({'min': min_bin, 'max': max_bin,
                                         'count': self._count_data_in_range(data, min_bin, max_bin)})

            return histogram_column

    def complete_histogram_attrs(self):
        """
        Complete histogram specific attributes
        :return:
        """
        range_of_date = self.max_x - self.min_x

        if not self.breaks:
            aggregated_data = self._get_aggregated_data()
            if self._get_default_histogram_width(aggregated_data):
                self.bins_width = self._get_default_histogram_width(aggregated_data)
                self.breaks = math.ceil(range_of_date / self.bins_width)
        else:
            self.bins_width = math.ceil(range_of_date / self.breaks)

        for column in self.columns:
            self._histogram_dictionary[column] = self._get_histogram_dictionary_for_column(column)