# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tdt.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Detrend(object):
    def setupUi(self, Detrend):
        Detrend.setObjectName("Detrend")
        Detrend.resize(857, 736)
        font = QtGui.QFont()
        font.setPointSize(9)
        Detrend.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("33_striker.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Detrend.setWindowIcon(icon)
        Detrend.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.gridLayout_2 = QtWidgets.QGridLayout(Detrend)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.extra_BJD = QtWidgets.QDoubleSpinBox(Detrend)
        self.extra_BJD.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.extra_BJD.setFont(font)
        self.extra_BJD.setDecimals(3)
        self.extra_BJD.setMinimum(-9999999.0)
        self.extra_BJD.setMaximum(9999999.0)
        self.extra_BJD.setProperty("value", 2457000.0)
        self.extra_BJD.setObjectName("extra_BJD")
        self.gridLayout.addWidget(self.extra_BJD, 6, 8, 1, 1)
        self.label = QtWidgets.QLabel(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.spline_wl = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spline_wl.setFont(font)
        self.spline_wl.setMinimum(0.1)
        self.spline_wl.setMaximum(2.0)
        self.spline_wl.setSingleStep(0.1)
        self.spline_wl.setProperty("value", 0.5)
        self.spline_wl.setObjectName("spline_wl")
        self.gridLayout.addWidget(self.spline_wl, 5, 3, 1, 1)
        self.reset_data = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.reset_data.setFont(font)
        self.reset_data.setObjectName("reset_data")
        self.gridLayout.addWidget(self.reset_data, 2, 8, 1, 1)
        self.kernel_size = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.kernel_size.setFont(font)
        self.kernel_size.setDecimals(1)
        self.kernel_size.setMaximum(100.0)
        self.kernel_size.setSingleStep(0.1)
        self.kernel_size.setProperty("value", 5.0)
        self.kernel_size.setObjectName("kernel_size")
        self.gridLayout.addWidget(self.kernel_size, 9, 3, 1, 1)
        self.comboBox_regs = QtWidgets.QComboBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_regs.setFont(font)
        self.comboBox_regs.setObjectName("comboBox_regs")
        self.gridLayout.addWidget(self.comboBox_regs, 8, 2, 1, 1)
        self.radio_remove_median = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_remove_median.setFont(font)
        self.radio_remove_median.setChecked(True)
        self.radio_remove_median.setObjectName("radio_remove_median")
        self.buttonGroup_trendOptions = QtWidgets.QButtonGroup(Detrend)
        self.buttonGroup_trendOptions.setObjectName("buttonGroup_trendOptions")
        self.buttonGroup_trendOptions.addButton(self.radio_remove_median)
        self.gridLayout.addWidget(self.radio_remove_median, 3, 0, 1, 1)
        self.saveProduct = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.saveProduct.setFont(font)
        self.saveProduct.setObjectName("saveProduct")
        self.gridLayout.addWidget(self.saveProduct, 8, 10, 1, 1)
        self.flatten_data = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.flatten_data.setFont(font)
        self.flatten_data.setChecked(True)
        self.flatten_data.setObjectName("flatten_data")
        self.buttonGroup_plot2 = QtWidgets.QButtonGroup(Detrend)
        self.buttonGroup_plot2.setObjectName("buttonGroup_plot2")
        self.buttonGroup_plot2.addButton(self.flatten_data)
        self.gridLayout.addWidget(self.flatten_data, 3, 10, 1, 1)
        self.GLS_of_data = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GLS_of_data.setFont(font)
        self.GLS_of_data.setObjectName("GLS_of_data")
        self.buttonGroup_plot2.addButton(self.GLS_of_data)
        self.gridLayout.addWidget(self.GLS_of_data, 4, 10, 1, 1)
        self.poly_wl = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.poly_wl.setFont(font)
        self.poly_wl.setMinimum(0.1)
        self.poly_wl.setMaximum(2.0)
        self.poly_wl.setSingleStep(0.1)
        self.poly_wl.setProperty("value", 0.5)
        self.poly_wl.setObjectName("poly_wl")
        self.gridLayout.addWidget(self.poly_wl, 6, 3, 1, 1)
        self.comboBox_poly = QtWidgets.QComboBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_poly.setFont(font)
        self.comboBox_poly.setObjectName("comboBox_poly")
        self.gridLayout.addWidget(self.comboBox_poly, 6, 2, 1, 1)
        self.label_wl = QtWidgets.QLabel(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_wl.setFont(font)
        self.label_wl.setObjectName("label_wl")
        self.gridLayout.addWidget(self.label_wl, 2, 3, 1, 1)
        self.regres_wl = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.regres_wl.setFont(font)
        self.regres_wl.setMinimum(0.1)
        self.regres_wl.setMaximum(2.0)
        self.regres_wl.setSingleStep(0.1)
        self.regres_wl.setProperty("value", 0.5)
        self.regres_wl.setObjectName("regres_wl")
        self.gridLayout.addWidget(self.regres_wl, 8, 3, 1, 1)
        self.comboBox_splines = QtWidgets.QComboBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_splines.setFont(font)
        self.comboBox_splines.setObjectName("comboBox_splines")
        self.gridLayout.addWidget(self.comboBox_splines, 5, 2, 1, 1)
        self.line = QtWidgets.QFrame(Detrend)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 9, 9, 1)
        self.comboBox_sliders = QtWidgets.QComboBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_sliders.setFont(font)
        self.comboBox_sliders.setObjectName("comboBox_sliders")
        self.gridLayout.addWidget(self.comboBox_sliders, 4, 2, 1, 1)
        self.spline_bt = QtWidgets.QDoubleSpinBox(Detrend)
        self.spline_bt.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spline_bt.setFont(font)
        self.spline_bt.setMaximum(1.0)
        self.spline_bt.setSingleStep(0.1)
        self.spline_bt.setProperty("value", 0.5)
        self.spline_bt.setObjectName("spline_bt")
        self.gridLayout.addWidget(self.spline_bt, 5, 4, 1, 1)
        self.click_to_reject = QtWidgets.QCheckBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.click_to_reject.setFont(font)
        self.click_to_reject.setObjectName("click_to_reject")
        self.gridLayout.addWidget(self.click_to_reject, 3, 7, 1, 2)
        self.add_epoch = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.add_epoch.setFont(font)
        self.add_epoch.setObjectName("add_epoch")
        self.gridLayout.addWidget(self.add_epoch, 6, 7, 1, 1)
        self.radio_Regressions = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_Regressions.setFont(font)
        self.radio_Regressions.setObjectName("radio_Regressions")
        self.buttonGroup_trendOptions.addButton(self.radio_Regressions)
        self.gridLayout.addWidget(self.radio_Regressions, 8, 0, 1, 2)
        self.regres_bt = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.regres_bt.setFont(font)
        self.regres_bt.setMaximum(1.0)
        self.regres_bt.setSingleStep(0.1)
        self.regres_bt.setProperty("value", 0.5)
        self.regres_bt.setObjectName("regres_bt")
        self.gridLayout.addWidget(self.regres_bt, 8, 4, 1, 1)
        self.poly_bt = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.poly_bt.setFont(font)
        self.poly_bt.setMaximum(1.0)
        self.poly_bt.setSingleStep(0.1)
        self.poly_bt.setProperty("value", 0.5)
        self.poly_bt.setObjectName("poly_bt")
        self.gridLayout.addWidget(self.poly_bt, 6, 4, 1, 1)
        self.GLS_of_model = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GLS_of_model.setFont(font)
        self.GLS_of_model.setObjectName("GLS_of_model")
        self.buttonGroup_plot2.addButton(self.GLS_of_model)
        self.gridLayout.addWidget(self.GLS_of_model, 6, 10, 1, 1)
        self.plot = PlotWidget(Detrend)
        self.plot.setMouseTracking(True)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 11)
        self.apply_dilution = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.apply_dilution.setFont(font)
        self.apply_dilution.setObjectName("apply_dilution")
        self.gridLayout.addWidget(self.apply_dilution, 9, 7, 1, 1)
        self.readme_button = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.readme_button.setFont(font)
        self.readme_button.setObjectName("readme_button")
        self.gridLayout.addWidget(self.readme_button, 9, 10, 1, 1)
        self.plot_2 = PlotWidget(Detrend)
        self.plot_2.setMouseTracking(True)
        self.plot_2.setObjectName("plot_2")
        self.gridLayout.addWidget(self.plot_2, 1, 0, 1, 11)
        self.radio_Splines = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_Splines.setFont(font)
        self.radio_Splines.setObjectName("radio_Splines")
        self.buttonGroup_trendOptions.addButton(self.radio_Splines)
        self.gridLayout.addWidget(self.radio_Splines, 5, 0, 1, 2)
        self.GLS_of_detr_data = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GLS_of_detr_data.setFont(font)
        self.GLS_of_detr_data.setObjectName("GLS_of_detr_data")
        self.buttonGroup_plot2.addButton(self.GLS_of_detr_data)
        self.gridLayout.addWidget(self.GLS_of_detr_data, 5, 10, 1, 1)
        self.radio_Polynomials = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_Polynomials.setFont(font)
        self.radio_Polynomials.setObjectName("radio_Polynomials")
        self.buttonGroup_trendOptions.addButton(self.radio_Polynomials)
        self.gridLayout.addWidget(self.radio_Polynomials, 6, 0, 1, 2)
        self.sliders_wl = QtWidgets.QDoubleSpinBox(Detrend)
        self.sliders_wl.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.sliders_wl.setFont(font)
        self.sliders_wl.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.sliders_wl.setMinimum(0.1)
        self.sliders_wl.setMaximum(2.0)
        self.sliders_wl.setSingleStep(0.1)
        self.sliders_wl.setProperty("value", 0.5)
        self.sliders_wl.setObjectName("sliders_wl")
        self.gridLayout.addWidget(self.sliders_wl, 4, 3, 1, 1)
        self.Dilution_fact = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Dilution_fact.setFont(font)
        self.Dilution_fact.setDecimals(3)
        self.Dilution_fact.setMinimum(0.01)
        self.Dilution_fact.setMaximum(1.0)
        self.Dilution_fact.setSingleStep(0.01)
        self.Dilution_fact.setProperty("value", 1.0)
        self.Dilution_fact.setObjectName("Dilution_fact")
        self.gridLayout.addWidget(self.Dilution_fact, 9, 8, 1, 1)
        self.comboBox_GP = QtWidgets.QComboBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_GP.setFont(font)
        self.comboBox_GP.setObjectName("comboBox_GP")
        self.gridLayout.addWidget(self.comboBox_GP, 9, 2, 1, 1)
        self.label_method = QtWidgets.QLabel(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_method.setFont(font)
        self.label_method.setObjectName("label_method")
        self.gridLayout.addWidget(self.label_method, 2, 2, 1, 1)
        self.try_button = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.try_button.setFont(font)
        self.try_button.setObjectName("try_button")
        self.gridLayout.addWidget(self.try_button, 2, 10, 1, 1)
        self.label_tolerance = QtWidgets.QLabel(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_tolerance.setFont(font)
        self.label_tolerance.setObjectName("label_tolerance")
        self.gridLayout.addWidget(self.label_tolerance, 2, 4, 1, 1)
        self.print_stat = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.print_stat.setFont(font)
        self.print_stat.setObjectName("print_stat")
        self.gridLayout.addWidget(self.print_stat, 2, 7, 1, 1)
        self.checkBox_GP_robust = QtWidgets.QCheckBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkBox_GP_robust.setFont(font)
        self.checkBox_GP_robust.setObjectName("checkBox_GP_robust")
        self.gridLayout.addWidget(self.checkBox_GP_robust, 9, 5, 1, 1)
        self.line_2 = QtWidgets.QFrame(Detrend)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 6, 8, 1)
        self.radio_GPs = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_GPs.setFont(font)
        self.radio_GPs.setObjectName("radio_GPs")
        self.buttonGroup_trendOptions.addButton(self.radio_GPs)
        self.gridLayout.addWidget(self.radio_GPs, 9, 0, 1, 2)
        self.radio_remove_mean = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_remove_mean.setFont(font)
        self.radio_remove_mean.setChecked(False)
        self.radio_remove_mean.setObjectName("radio_remove_mean")
        self.buttonGroup_trendOptions.addButton(self.radio_remove_mean)
        self.gridLayout.addWidget(self.radio_remove_mean, 3, 1, 1, 1)
        self.GP_period = QtWidgets.QDoubleSpinBox(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GP_period.setFont(font)
        self.GP_period.setObjectName("GP_period")
        self.gridLayout.addWidget(self.GP_period, 9, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 5, 1, 1)
        self.bin_data = QtWidgets.QDoubleSpinBox(Detrend)
        self.bin_data.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bin_data.setFont(font)
        self.bin_data.setSuffix("")
        self.bin_data.setDecimals(5)
        self.bin_data.setMinimum(1e-05)
        self.bin_data.setSingleStep(0.001)
        self.bin_data.setProperty("value", 0.01)
        self.bin_data.setObjectName("bin_data")
        self.gridLayout.addWidget(self.bin_data, 5, 8, 1, 1)
        self.radio_timeW = QtWidgets.QRadioButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.radio_timeW.setFont(font)
        self.radio_timeW.setObjectName("radio_timeW")
        self.buttonGroup_trendOptions.addButton(self.radio_timeW)
        self.gridLayout.addWidget(self.radio_timeW, 4, 0, 1, 2)
        self.button_bin_data = QtWidgets.QPushButton(Detrend)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.button_bin_data.setFont(font)
        self.button_bin_data.setObjectName("button_bin_data")
        self.gridLayout.addWidget(self.button_bin_data, 5, 7, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Detrend)
        QtCore.QMetaObject.connectSlotsByName(Detrend)

    def retranslateUi(self, Detrend):
        _translate = QtCore.QCoreApplication.translate
        Detrend.setWindowTitle(_translate("Detrend", "Detrend"))
        self.label.setText(_translate("Detrend", "Normalization"))
        self.reset_data.setText(_translate("Detrend", "Reset"))
        self.radio_remove_median.setText(_translate("Detrend", "Median"))
        self.saveProduct.setText(_translate("Detrend", "Save detr. data"))
        self.flatten_data.setText(_translate("Detrend", "detrended data"))
        self.GLS_of_data.setText(_translate("Detrend", "GLS of input data"))
        self.label_wl.setText(_translate("Detrend", "Window length"))
        self.click_to_reject.setText(_translate("Detrend", "remove outliers"))
        self.add_epoch.setText(_translate("Detrend", "Add/Remove BJD"))
        self.radio_Regressions.setText(_translate("Detrend", "Regressions"))
        self.GLS_of_model.setText(_translate("Detrend", "GLS of model"))
        self.apply_dilution.setText(_translate("Detrend", "Apply Dilution fact."))
        self.readme_button.setText(_translate("Detrend", "READ ME"))
        self.radio_Splines.setText(_translate("Detrend", "Splines"))
        self.GLS_of_detr_data.setText(_translate("Detrend", "GLS of detr. data"))
        self.radio_Polynomials.setText(_translate("Detrend", "Polynomials"))
        self.label_method.setText(_translate("Detrend", "Method"))
        self.try_button.setText(_translate("Detrend", "Try!"))
        self.label_tolerance.setText(_translate("Detrend", "Break tolerance"))
        self.print_stat.setText(_translate("Detrend", "Print stat"))
        self.checkBox_GP_robust.setText(_translate("Detrend", "robust"))
        self.radio_GPs.setText(_translate("Detrend", "Gaussian Processes"))
        self.radio_remove_mean.setText(_translate("Detrend", "Mean"))
        self.radio_timeW.setText(_translate("Detrend", "Time-windowed "))
        self.button_bin_data.setText(_translate("Detrend", "Bin data [d]"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Detrend = QtWidgets.QWidget()
    ui = Ui_Detrend()
    ui.setupUi(Detrend)
    Detrend.show()
    sys.exit(app.exec_())
