#!/usr/bin/python
__author__ = 'Trifon Trifonov'

import numpy as np
#import matplotlib as mpl
#mpl.use('Qt5Agg')
import sys, os, traceback 
from PyQt5 import QtCore, QtGui, QtWidgets, uic

sys.path.insert(0, './lib')

import RV_mod as rv

import pyqtgraph as pg
import pyqtgraph.console as pg_console

import word_processor_es as text_editor_es
import calculator as calc 
import gls as gls 
from worker import Worker #, WorkerSignals

#from multiprocessing import cpu_count
#import time

#import BKR as bkr
from doublespinbox import DoubleSpinBox
from Jupyter_emb import ConsoleWidget_embed
from stdout_pipe import MyDialog
from print_info_window import print_info
from symbols_window import show_symbols

import terminal
from tree_view import Widget_tree

import ntpath

from scipy.signal import argrelextrema
from scipy.stats.stats import pearsonr   

import batman as batman

try:
    from transitleastsquares import transitleastsquares    
    tls_not_found = False 
except (ImportError, KeyError) as e:
    tls_not_found = True
    pass               
       

    
import webbrowser
 
#try:
#    import cPickle as pickle
#except ModuleNotFoundError:
#    import pickle
import dill


#if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
#    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

#if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
#    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,True)



qtCreatorFile = "./lib/UI/rvmod_gui.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

pg.setConfigOption('background', '#ffffff')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)  
 
 


global fit, colors, ses_list
 

fit=rv.signal_fit(name='init')
ses_list = [fit]
 


colors  = ['#0066ff',  '#ff0000','#66ff66','#00ffff','#cc33ff','#ff9900','#cccc00','#3399ff','#990033','#339933','#666699']
symbols = ['o','t','t1','t2','t3','s','p','h','star','+','d'] 

QtGui.QApplication.processEvents()

 

 
class TRIFON(QtWidgets.QMainWindow, Ui_MainWindow):

    def update_labels(self):
        global fit

 
        self.value_stellar_mass.setText("%.2f"%(fit.params.stellar_mass))
        self.value_epoch.setText(str(fit.epoch))
        self.value_rms.setText("%.4f"%(fit.fit_results.rms))
        self.value_chi2.setText("%.4f"%(fit.fit_results.chi2)) 
        self.value_reduced_chi2.setText("%.4f"%(fit.fit_results.reduced_chi2))        
        #self.value_loglik.setText("%.4f"%(fit.fit_results.loglik)) 
        self.value_loglik.setText("%.4f"%(fit.loglik)) 
       
        self.value_Ndata.setText("%s"%(len(fit.fit_results.jd))) 
        self.value_DOF.setText("%s"%(len(fit.fit_results.jd) - fit.fit_results.mfit))        

        if fit.mod_dynamical == True:
            self.radioButton_Dynamical.setChecked(True)        
        else:
            self.radioButton_Keplerian.setChecked(True)        

    def update_gui_params(self):
        global fit

        param_gui = [self.K1, self.P1, self.e1, self.om1, self.ma1, self.incl1, self.Omega1,
                     self.K2, self.P2, self.e2, self.om2, self.ma2, self.incl2, self.Omega2,
                     self.K3, self.P3, self.e3, self.om3, self.ma3, self.incl3, self.Omega3,
                     self.K4, self.P4, self.e4, self.om4, self.ma4, self.incl4, self.Omega4, 
                     self.K5, self.P5, self.e5, self.om5, self.ma5, self.incl5, self.Omega5,
                     self.K6, self.P6, self.e6, self.om6, self.ma6, self.incl6, self.Omega6,
                     self.K7, self.P7, self.e7, self.om7, self.ma7, self.incl7, self.Omega7, 
                     self.K8, self.P8, self.e8, self.om8, self.ma8, self.incl8, self.Omega8,
                     self.K9, self.P9, self.e9, self.om9, self.ma9, self.incl9, self.Omega9,
                     ]
         
        for i in range(fit.npl*7):
            param_gui[i].setValue(fit.params.planet_params[i]) 
            
            
       # param_gui_trans = [self.t0_1_trans, self.P1_trans, self.e1_trans, self.om1_trans, self.pl1_radii, self.incl1_trans, self.a1_trans,]     
        
      #  for i in range(len(param_gui_trans)):
      #      param_gui_trans[i].setValue(fit.tr_par[i])
            
        param_gui_tr = [self.t0_1, self.pl_rad_1, self.a_sol_1,
                     self.t0_2, self.pl_rad_2, self.a_sol_2,
                     self.t0_3, self.pl_rad_3, self.a_sol_3,
                     self.t0_4, self.pl_rad_4, self.a_sol_4, 
                     self.t0_5, self.pl_rad_5, self.a_sol_5,
                     self.t0_6, self.pl_rad_6, self.a_sol_6,
                     self.t0_7, self.pl_rad_7, self.a_sol_7, 
                     self.t0_8, self.pl_rad_8, self.a_sol_8,
                     self.t0_9, self.pl_rad_9, self.a_sol_9,
                     ]
         
        for i in range(fit.npl):
            param_gui_tr[i*3].setValue(fit.t0[i])           
            param_gui_tr[i*3+1].setValue(fit.pl_rad[i]) 
            param_gui_tr[i*3+2].setValue(fit.pl_a[i]) 
            
        rvs_data_gui = [self.Data1,self.Data2,self.Data3,self.Data4,self.Data5,
                    self.Data6,self.Data7,self.Data8,self.Data9,self.Data10]
        rvs_data_jitter_gui = [self.jitter_Data1,self.jitter_Data2,self.jitter_Data3,self.jitter_Data4,self.jitter_Data5,
                           self.jitter_Data6,self.jitter_Data7,self.jitter_Data8,self.jitter_Data9,self.jitter_Data10]

        for i in range(10): 
            rvs_data_gui[i].setValue(fit.params.offsets[i]) 
            rvs_data_jitter_gui[i].setValue(fit.params.jitters[i])
        
        tra_data_gui = [self.trans_Data1,self.trans_Data2,self.trans_Data3,self.trans_Data4,self.trans_Data5,
                        self.trans_Data6,self.trans_Data7,self.trans_Data8,self.trans_Data9,self.trans_Data10]
        tra_data_jitter_gui = [self.jitter_trans_Data1,self.jitter_trans_Data2,self.jitter_trans_Data3,self.jitter_trans_Data4,self.jitter_trans_Data5,
                               self.jitter_trans_Data6,self.jitter_trans_Data7,self.jitter_trans_Data8,self.jitter_trans_Data9,self.jitter_trans_Data10]
        
            
        for i in range(10): 
            tra_data_gui[i].setValue(fit.tra_off[i]) 
            tra_data_jitter_gui[i].setValue(fit.tra_jitt[i])            
            
        gp_rot_params = [self.GP_rot_kernel_Amp,
                     self.GP_rot_kernel_time_sc,
                     self.GP_rot_kernel_Per,
                     self.GP_rot_kernel_fact]
        
        for i in range(len(gp_rot_params)):
            gp_rot_params[i].setValue(fit.GP_rot_params[i])
 
        gp_sho_params = [self.GP_sho_kernel_S,
                     self.GP_sho_kernel_Q,
                     self.GP_sho_kernel_omega]
        
        for i in range(len(gp_sho_params)):
            gp_sho_params[i].setValue(fit.GP_sho_params[i])            

            
        self.St_mass_input.setValue(fit.params.stellar_mass)        
        self.RV_lin_trend.setValue(fit.params.linear_trend)   
        self.Epoch.setValue(fit.epoch)


    def update_params(self):
        global fit

        param_gui = [self.K1, self.P1, self.e1, self.om1, self.ma1, self.incl1, self.Omega1,
                     self.K2, self.P2, self.e2, self.om2, self.ma2, self.incl2, self.Omega2,
                     self.K3, self.P3, self.e3, self.om3, self.ma3, self.incl3, self.Omega3,
                     self.K4, self.P4, self.e4, self.om4, self.ma4, self.incl4, self.Omega4, 
                     self.K5, self.P5, self.e5, self.om5, self.ma5, self.incl5, self.Omega5,
                     self.K6, self.P6, self.e6, self.om6, self.ma6, self.incl6, self.Omega6,
                     self.K7, self.P7, self.e7, self.om7, self.ma7, self.incl7, self.Omega7, 
                     self.K8, self.P8, self.e8, self.om8, self.ma8, self.incl8, self.Omega8,
                     self.K9, self.P9, self.e9, self.om9, self.ma9, self.incl9, self.Omega9,
                     ]
                     

        for i in range(fit.npl*7):
            fit.params.planet_params[i] = param_gui[i].value() 
            
            
       # param_gui_trans = [self.t0_1_trans, self.P1_trans, self.e1_trans, self.om1_trans,self.pl1_radii, self.incl1_trans, self.a1_trans,]
         
       ## for i in range(len(param_gui_trans)):
       #     fit.tr_par[i] = param_gui_trans[i].value()    

       # fit.update_trans_params()  
        
        
        param_gui_tr = [self.t0_1, self.pl_rad_1, self.a_sol_1,
             self.t0_2, self.pl_rad_2, self.a_sol_2,
             self.t0_3, self.pl_rad_3, self.a_sol_3,
             self.t0_4, self.pl_rad_4, self.a_sol_4, 
             self.t0_5, self.pl_rad_5, self.a_sol_5,
             self.t0_6, self.pl_rad_6, self.a_sol_6,
             self.t0_7, self.pl_rad_7, self.a_sol_7, 
             self.t0_8, self.pl_rad_8, self.a_sol_8,
             self.t0_9, self.pl_rad_9, self.a_sol_9,
             ]
         
        for i in range(fit.npl):
            fit.t0[i]     = param_gui_tr[i*3].value()   
            fit.pl_rad[i] = param_gui_tr[i*3+1].value() 
            fit.pl_a[i]   = param_gui_tr[i*3+2].value() 




        rvs_data_gui = [self.Data1,self.Data2,self.Data3,self.Data4,self.Data5,
                    self.Data6,self.Data7,self.Data8,self.Data9,self.Data10]
        rvs_data_jitter_gui = [self.jitter_Data1,self.jitter_Data2,self.jitter_Data3,self.jitter_Data4,self.jitter_Data5,
                           self.jitter_Data6,self.jitter_Data7,self.jitter_Data8,self.jitter_Data9,self.jitter_Data10]

        for i in range(10): 
            fit.params.offsets[i] = rvs_data_gui[i].value() 
            fit.params.jitters[i] = rvs_data_jitter_gui[i].value()

        tra_data_gui = [self.trans_Data1,self.trans_Data2,self.trans_Data3,self.trans_Data4,self.trans_Data5,
                        self.trans_Data6,self.trans_Data7,self.trans_Data8,self.trans_Data9,self.trans_Data10]
        tra_data_jitter_gui = [self.jitter_trans_Data1,self.jitter_trans_Data2,self.jitter_trans_Data3,self.jitter_trans_Data4,self.jitter_trans_Data5,
                               self.jitter_trans_Data6,self.jitter_trans_Data7,self.jitter_trans_Data8,self.jitter_trans_Data9,self.jitter_trans_Data10]
        
            
        for i in range(10): 
            fit.tra_off[i]  = tra_data_gui[i].value() 
            fit.tra_jitt[i] = tra_data_jitter_gui[i].value() 
 
            
        gp_rot_params = [self.GP_rot_kernel_Amp,
                     self.GP_rot_kernel_time_sc,
                     self.GP_rot_kernel_Per,
                     self.GP_rot_kernel_fact]
        
        for i in range(len(gp_rot_params)):
            fit.GP_rot_params[i] = gp_rot_params[i].value()    
            
            
        gp_sho_params = [self.GP_sho_kernel_S,
                     self.GP_sho_kernel_Q,
                     self.GP_sho_kernel_omega]
        
        for i in range(len(gp_sho_params)):
            fit.GP_sho_params[i] = gp_sho_params[i].value()              
            
            
  

        fit.params.stellar_mass = self.St_mass_input.value() 
        fit.params.linear_trend = self.RV_lin_trend.value()   
        
        if self.checkBox_first_RV_epoch.isChecked() and len(fit.fit_results.rv_model.jd) != 0:
            fit.epoch = min(fit.fit_results.rv_model.jd)
        else:
            fit.epoch =  self.Epoch.value()
       


    def update_errors(self):
        global fit

        param_errors_gui = [self.err_K1,self.err_P1,self.err_e1,self.err_om1,self.err_ma1, self.err_i1, self.err_Om1,
                            self.err_K2,self.err_P2,self.err_e2,self.err_om2,self.err_ma2, self.err_i2, self.err_Om2,
                            self.err_K3,self.err_P3,self.err_e3,self.err_om3,self.err_ma3, self.err_i3, self.err_Om3,
                            self.err_K4,self.err_P4,self.err_e4,self.err_om4,self.err_ma4, self.err_i4, self.err_Om4,  
                            self.err_K5,self.err_P5,self.err_e5,self.err_om5,self.err_ma5, self.err_i5, self.err_Om5,
                            self.err_K6,self.err_P6,self.err_e6,self.err_om6,self.err_ma6, self.err_i6, self.err_Om6,
                            self.err_K7,self.err_P7,self.err_e7,self.err_om7,self.err_ma7, self.err_i7, self.err_Om7, 
                            self.err_K8,self.err_P8,self.err_e8,self.err_om8,self.err_ma8, self.err_i8, self.err_Om8,
                            self.err_K9,self.err_P9,self.err_e9,self.err_om9,self.err_ma9, self.err_i9, self.err_Om9,                       
                            ]
        for i in range(fit.npl*7):
            param_errors_gui[i].setText("+/- %.3f"%max(np.abs(fit.param_errors.planet_params_errors[i])))


        data_errors_gui        = [self.err_Data1,self.err_Data2,self.err_Data3,self.err_Data4,self.err_Data5,
                                  self.err_Data6,self.err_Data7,self.err_Data8,self.err_Data9,self.err_Data10]
        data_errors_jitter_gui = [self.err_jitter_Data1,self.err_jitter_Data2,self.err_jitter_Data3,self.err_jitter_Data4,
                                  self.err_jitter_Data5,self.err_jitter_Data6,self.err_jitter_Data7,self.err_jitter_Data8,
                                  self.err_jitter_Data9,self.err_jitter_Data10]

        for i in range(10):
            data_errors_gui[i].setText("+/- %.3f"%max(np.abs(fit.param_errors.offset_errors[i])))
            data_errors_jitter_gui[i].setText("+/- %.3f"%max(np.abs(fit.param_errors.jitter_errors[i])))
            
        tra_data_errors_gui        = [self.err_trans_Data1,self.err_trans_Data2,self.err_trans_Data3,self.err_trans_Data4,self.err_trans_Data5,
                                      self.err_trans_Data6,self.err_trans_Data7,self.err_trans_Data8,self.err_trans_Data9,self.err_trans_Data10]
        tra_data_errors_jitter_gui = [self.err_jitter_trans_Data1,self.err_jitter_trans_Data2,self.err_jitter_trans_Data3,self.err_jitter_trans_Data4,
                                      self.err_jitter_trans_Data5,self.err_jitter_trans_Data6,self.err_jitter_trans_Data7,self.err_jitter_trans_Data8,
                                      self.err_jitter_trans_Data9,self.err_jitter_trans_Data10]

        for i in range(10):
            tra_data_errors_gui[i].setText("+/- %.3f"%max(np.abs(fit.tra_off_err[i])))
            tra_data_errors_jitter_gui[i].setText("+/- %.3f"%max(np.abs(fit.tra_jitt_err[i])))            
            
            

        self.err_RV_lin_trend.setText("+/- %.8f"%(max(fit.param_errors.linear_trend_error)))
        
        gp_rot_errors_gui = [self.err_rot_kernel_Amp,
                     self.err_rot_kernel_time_sc,
                     self.err_rot_kernel_Per,
                     self.err_rot_kernel_fact]
        
        for i in range(len(gp_rot_errors_gui)):
            gp_rot_errors_gui[i].setText("+/- %.3f"%max(np.abs(fit.param_errors.GP_params_errors[i])))  
            
        gp_sho_errors_gui = [self.err_sho_kernel_S,
                     self.err_sho_kernel_Q,
                     self.err_sho_kernel_omega]
        
        #for i in range(len(gp_rot_errors_gui)):
       #     gp_rot_errors_gui[i].setText("+/- %.3f"%max(np.abs(fit.param_errors.GP_sho_params_errors[i])))              
            
            
 #        GP_params_errors


    def update_a_mass(self):
        global fit

        param_a_gui = [self.label_a1, self.label_a2, self.label_a3, self.label_a4, self.label_a5, 
                       self.label_a6, self.label_a7, self.label_a8, self.label_a9]
        param_mass_gui = [self.label_mass1, self.label_mass2, self.label_mass3, self.label_mass4, self.label_mass5, 
                       self.label_mass6, self.label_mass7, self.label_mass8, self.label_mass9]
        param_t_peri_gui = [self.label_t_peri1, self.label_t_peri2, self.label_t_peri3, self.label_t_peri4, self.label_t_peri5, 
                       self.label_t_peri6, self.label_t_peri7, self.label_t_peri8, self.label_t_peri9]

        if self.radioButton_RV.isChecked():
            for i in range(fit.npl):
                param_a_gui[i].setText("%.3f"%(fit.fit_results.a[i])) 
                param_mass_gui[i].setText("%.3f"%(fit.fit_results.mass[i])) 
                #param_t_peri_gui[i].setText("%.3f"%( (float(fit.epoch) - (np.radians(fit.params.planet_params[7*i + 4])/(2*np.pi))*fit.params.planet_params[7*i + 1] ))) # epoch  - ((ma/TWOPI)*a[1])
                param_t_peri_gui[i].setText("%.3f"%(fit.t_peri[i]))




    def update_use_from_input_file(self):
        global fit


        use_param_gui =  [self.use_K1, self.use_P1, self.use_e1, self.use_om1, self.use_ma1, self.use_incl1, self.use_Omega1,
                          self.use_K2, self.use_P2, self.use_e2, self.use_om2, self.use_ma2, self.use_incl2, self.use_Omega2,
                          self.use_K3, self.use_P3, self.use_e3, self.use_om3, self.use_ma3, self.use_incl3, self.use_Omega3,                        
                          self.use_K4, self.use_P4, self.use_e4, self.use_om4, self.use_ma4, self.use_incl4, self.use_Omega4,    
                          self.use_K5, self.use_P5, self.use_e5, self.use_om5, self.use_ma5, self.use_incl5, self.use_Omega5,    
                          self.use_K6, self.use_P6, self.use_e6, self.use_om6, self.use_ma6, self.use_incl6, self.use_Omega6, 
                          self.use_K7, self.use_P7, self.use_e7, self.use_om7, self.use_ma7, self.use_incl7, self.use_Omega7,    
                          self.use_K8, self.use_P8, self.use_e8, self.use_om8, self.use_ma8, self.use_incl8, self.use_Omega8,    
                          self.use_K9, self.use_P9, self.use_e9, self.use_om9, self.use_ma9, self.use_incl9, self.use_Omega9,                       
                          ]
        
        for i in range(fit.npl*7):
            use_param_gui[i].setChecked(bool(fit.use.use_planet_params[i]))

       # use_param_gui_trans = [self.use_t0_1_trans, self.use_P1_trans, self.use_e1_trans, self.use_om1_trans, self.use_pl1_rad_trans, self.use_incl1_trans, self.use_a1_trans,
      #               ]
         
      #  for i in range(len(use_param_gui_trans)):
       #     use_param_gui_trans[i].setChecked(bool(  fit.tr_params_use[i] ))   
            
            
        use_param_gui_tr = [self.use_t0_1, self.use_pl_rad_1, self.use_a_sol_1,
             self.use_t0_2, self.use_pl_rad_2, self.use_a_sol_2,
             self.use_t0_3, self.use_pl_rad_3, self.use_a_sol_3,
             self.use_t0_4, self.use_pl_rad_4, self.use_a_sol_4, 
             self.use_t0_5, self.use_pl_rad_5, self.use_a_sol_5,
             self.use_t0_6, self.use_pl_rad_6, self.use_a_sol_6,
             self.use_t0_7, self.use_pl_rad_7, self.use_a_sol_7, 
             self.use_t0_8, self.use_pl_rad_8, self.use_a_sol_8,
             self.use_t0_9, self.use_pl_rad_9, self.use_a_sol_9,
             ]
         
        for i in range(fit.npl):         
            use_param_gui_tr[i*3].setChecked(bool(fit.t0_use[i]) )        
            use_param_gui_tr[i*3+1].setChecked(bool(fit.pl_rad_use[i]) )
            use_param_gui_tr[i*3+2].setChecked(bool(fit.pl_a_use [i]) )
                        
            


        use_data_offset_gui = [self.use_offset_Data1,self.use_offset_Data2,self.use_offset_Data3,self.use_offset_Data4,
                               self.use_offset_Data5,self.use_offset_Data6,self.use_offset_Data7,self.use_offset_Data8,
                               self.use_offset_Data9,self.use_offset_Data10]
        use_data_jitter_gui = [self.use_jitter_Data1,self.use_jitter_Data2,self.use_jitter_Data3,self.use_jitter_Data4,self.use_jitter_Data5,
                               self.use_jitter_Data6,self.use_jitter_Data7,self.use_jitter_Data8,self.use_jitter_Data9,self.use_jitter_Data10]

        for i in range(10): 
            #use_data_gui[i].setChecked(bool(fit.use.use_offsets[i])) # attention, TBF
            use_data_jitter_gui[i].setChecked(bool(fit.use.use_jitters[i]))
            use_data_offset_gui[i].setChecked(bool(fit.use.use_offsets[i])) 
            
            
        use_tra_data_offset_gui = [self.use_offset_trans_Data1,self.use_offset_trans_Data2,self.use_offset_trans_Data3,self.use_offset_trans_Data4,
                                   self.use_offset_trans_Data5,self.use_offset_trans_Data6,self.use_offset_trans_Data7,self.use_offset_trans_Data8,
                                   self.use_offset_trans_Data9,self.use_offset_trans_Data10]
        use_tra_data_jitter_gui = [self.use_jitter_trans_Data1,self.use_jitter_trans_Data2,self.use_jitter_trans_Data3,self.use_jitter_trans_Data4,self.use_jitter_trans_Data5,
                                   self.use_jitter_trans_Data6,self.use_jitter_trans_Data7,self.use_jitter_trans_Data8,self.use_jitter_trans_Data9,self.use_jitter_trans_Data10]

        for i in range(10): 
            #use_data_gui[i].setChecked(bool(fit.use.use_offsets[i])) # attention, TBF
            use_tra_data_jitter_gui[i].setChecked(bool(fit.tra_jitt_use[i]))
            use_tra_data_offset_gui[i].setChecked(bool(fit.tra_off_use[i]))             
            

        planet_checked_gui = [self.use_Planet1,self.use_Planet2,self.use_Planet3,self.use_Planet4,self.use_Planet5,
                              self.use_Planet6,self.use_Planet7,self.use_Planet8,self.use_Planet9]
        for i in range(9):  
            if i < fit.npl:
                planet_checked_gui[i].setChecked(True)  
            else:
                planet_checked_gui[i].setChecked(False)  
            
        self.use_RV_lin_trend.setChecked(bool(fit.use.use_linear_trend)) 
        

        use_gp_rot_params = [self.use_GP_rot_kernel_Amp,
                         self.use_GP_rot_kernel_time_sc,
                         self.use_GP_rot_kernel_Per,
                         self.use_GP_rot_kernel_fact]
                    
        
        for i in range(len(use_gp_rot_params)):
            use_gp_rot_params[i].setChecked(bool(fit.GP_rot_use[i]))
 
    
        use_gp_sho_params = [self.use_GP_sho_kernel_S,
                         self.use_GP_sho_kernel_Q,
                         self.use_GP_sho_kernel_omega]
                    
        
        for i in range(len(use_gp_sho_params)):
            use_gp_sho_params[i].setChecked(bool(fit.GP_sho_use[i]))


    def update_mixed_fitting(self):
        global fit
        
        fit.mixed_fit[0] =  int(self.use_mix_fitting.isChecked())
        fit.mixed_fit[1] = [int(self.mix_pl_1.isChecked()),int(self.mix_pl_2.isChecked()),int(self.mix_pl_3.isChecked()),
                            int(self.mix_pl_4.isChecked()),int(self.mix_pl_5.isChecked()),int(self.mix_pl_6.isChecked()),
                            int(self.mix_pl_7.isChecked()),int(self.mix_pl_8.isChecked()),int(self.mix_pl_9.isChecked()),
                            ]       
        
        
            
    def update_use(self):
        global fit
        
        use_planet_gui = [self.use_Planet1,self.use_Planet2,self.use_Planet3,self.use_Planet4,self.use_Planet5,
                          self.use_Planet6,self.use_Planet7,self.use_Planet8,self.use_Planet9]
        #for i in range(len(use_planet_gui)):  
        npl_old = fit.npl
        checked = int(np.sum( [use_planet_gui[i].isChecked() for i in range(len(use_planet_gui))] ))
 
        if npl_old < checked:
            fit.add_planet()
        elif npl_old >= checked:
            fit.npl = checked     
            
        #for i in range(len(use_planet_gui)):
        #    if use_planet_gui[i].isChecked() == False:
       #         fit.remove_planet(i)  
       #     else:
       #         fit.add_planet(i)  
       #         

        use_param_gui = [self.use_K1, self.use_P1, self.use_e1, self.use_om1, self.use_ma1, self.use_incl1, self.use_Omega1,
                          self.use_K2, self.use_P2, self.use_e2, self.use_om2, self.use_ma2, self.use_incl2, self.use_Omega2,
                          self.use_K3, self.use_P3, self.use_e3, self.use_om3, self.use_ma3, self.use_incl3, self.use_Omega3,                        
                          self.use_K4, self.use_P4, self.use_e4, self.use_om4, self.use_ma4, self.use_incl4, self.use_Omega4,    
                          self.use_K5, self.use_P5, self.use_e5, self.use_om5, self.use_ma5, self.use_incl5, self.use_Omega5,    
                          self.use_K6, self.use_P6, self.use_e6, self.use_om6, self.use_ma6, self.use_incl6, self.use_Omega6, 
                          self.use_K7, self.use_P7, self.use_e7, self.use_om7, self.use_ma7, self.use_incl7, self.use_Omega7,    
                          self.use_K8, self.use_P8, self.use_e8, self.use_om8, self.use_ma8, self.use_incl8, self.use_Omega8,    
                          self.use_K9, self.use_P9, self.use_e9, self.use_om9, self.use_ma9, self.use_incl9, self.use_Omega9,                       
                          ]

        for i in range(fit.npl*7):
            fit.use.use_planet_params[i] = int(use_param_gui[i].isChecked())         
            
       # use_param_gui_trans = [self.use_t0_1_trans, self.use_P1_trans, self.use_e1_trans, self.use_om1_trans, self.use_pl1_rad_trans, self.use_incl1_trans, self.use_a1_trans,
       #              ]
         
        #for i in range(len(use_param_gui_trans)):
       #     fit.tr_params_use[i] =  use_param_gui_trans[i].isChecked()       
            
        use_param_gui_tr = [self.use_t0_1, self.use_pl_rad_1, self.use_a_sol_1,
             self.use_t0_2, self.use_pl_rad_2, self.use_a_sol_2,
             self.use_t0_3, self.use_pl_rad_3, self.use_a_sol_3,
             self.use_t0_4, self.use_pl_rad_4, self.use_a_sol_4, 
             self.use_t0_5, self.use_pl_rad_5, self.use_a_sol_5,
             self.use_t0_6, self.use_pl_rad_6, self.use_a_sol_6,
             self.use_t0_7, self.use_pl_rad_7, self.use_a_sol_7, 
             self.use_t0_8, self.use_pl_rad_8, self.use_a_sol_8,
             self.use_t0_9, self.use_pl_rad_9, self.use_a_sol_9,
             ]
         
        for i in range(fit.npl):        
            #print('test')
            fit.t0_use[i] =  use_param_gui_tr[i*3].isChecked()  
            fit.pl_rad_use[i] = use_param_gui_tr[i*3+1].isChecked()  
            fit.pl_a_use [i] =  use_param_gui_tr[i*3+2].isChecked()  
       
            
            

        use_data_offset_gui = [self.use_offset_Data1,self.use_offset_Data2,self.use_offset_Data3,self.use_offset_Data4,
                               self.use_offset_Data5,self.use_offset_Data6,self.use_offset_Data7,self.use_offset_Data8,
                               self.use_offset_Data9,self.use_offset_Data10]
        use_data_jitter_gui = [self.use_jitter_Data1,self.use_jitter_Data2,self.use_jitter_Data3,self.use_jitter_Data4,self.use_jitter_Data5,
                               self.use_jitter_Data6,self.use_jitter_Data7,self.use_jitter_Data8,self.use_jitter_Data9,self.use_jitter_Data10]

        for i in range(10): 
            fit.use.use_jitters[i] = int(use_data_jitter_gui[i].isChecked())
            fit.use.use_offsets[i] = int(use_data_offset_gui[i].isChecked())   


        use_tra_data_offset_gui = [self.use_offset_trans_Data1,self.use_offset_trans_Data2,self.use_offset_trans_Data3,self.use_offset_trans_Data4,
                                   self.use_offset_trans_Data5,self.use_offset_trans_Data6,self.use_offset_trans_Data7,self.use_offset_trans_Data8,
                                   self.use_offset_trans_Data9,self.use_offset_trans_Data10]
        use_tra_data_jitter_gui = [self.use_jitter_trans_Data1,self.use_jitter_trans_Data2,self.use_jitter_trans_Data3,self.use_jitter_trans_Data4,self.use_jitter_trans_Data5,
                                   self.use_jitter_trans_Data6,self.use_jitter_trans_Data7,self.use_jitter_trans_Data8,self.use_jitter_trans_Data9,self.use_jitter_trans_Data10]

        for i in range(10): 
            fit.tra_jitt_use[i] = int(use_tra_data_jitter_gui[i].isChecked())
            fit.tra_off_use[i]  = int(use_tra_data_offset_gui[i].isChecked())
 
 

        fit.use.use_linear_trend = int(self.use_RV_lin_trend.isChecked()) 


        use_gp_rot_params = [self.use_GP_rot_kernel_Amp,
                         self.use_GP_rot_kernel_time_sc,
                         self.use_GP_rot_kernel_Per,
                         self.use_GP_rot_kernel_fact]
                    
        
        for i in range(len(use_gp_rot_params)):
            fit.GP_rot_use[i] = int(use_gp_rot_params[i].isChecked())
            
        use_gp_sho_params = [self.use_GP_sho_kernel_S,
                         self.use_GP_sho_kernel_Q,
                         self.use_GP_sho_kernel_omega]
                    
        
        for i in range(len(use_gp_sho_params)):
            fit.GP_sho_use[i] = int(use_gp_sho_params[i].isChecked())            
            
            
            
 
   
    def check_bounds(self):
        global fit

        
        
        param_bounds_gui = [
        [self.K_min_1.value(),self.K_max_1.value()],[self.P_min_1.value(),self.P_max_1.value()], [self.e_min_1.value(),self.e_max_1.value()],[self.om_min_1.value(),self.om_max_1.value()], [self.ma_min_1.value(),self.ma_max_1.value()],[self.incl_min_1.value(),self.incl_max_1.value()], [self.Omega_min_1.value(),self.Omega_max_1.value()],[self.t0_min_1.value(),self.t0_max_1.value()],[self.pl_rad_min_1.value(),self.pl_rad_max_1.value()],[self.a_sol_min_1.value(),self.a_sol_max_1.value()],
        [self.K_min_2.value(),self.K_max_2.value()],[self.P_min_2.value(),self.P_max_2.value()], [self.e_min_2.value(),self.e_max_2.value()],[self.om_min_2.value(),self.om_max_2.value()], [self.ma_min_2.value(),self.ma_max_2.value()],[self.incl_min_2.value(),self.incl_max_2.value()], [self.Omega_min_2.value(),self.Omega_max_2.value()],[self.t0_min_2.value(),self.t0_max_2.value()],[self.pl_rad_min_2.value(),self.pl_rad_max_2.value()],[self.a_sol_min_2.value(),self.a_sol_max_2.value()],
        [self.K_min_3.value(),self.K_max_3.value()],[self.P_min_3.value(),self.P_max_3.value()], [self.e_min_3.value(),self.e_max_3.value()],[self.om_min_3.value(),self.om_max_3.value()], [self.ma_min_3.value(),self.ma_max_3.value()],[self.incl_min_3.value(),self.incl_max_3.value()], [self.Omega_min_3.value(),self.Omega_max_3.value()],[self.t0_min_3.value(),self.t0_max_3.value()],[self.pl_rad_min_3.value(),self.pl_rad_max_3.value()],[self.a_sol_min_3.value(),self.a_sol_max_3.value()],
        [self.K_min_4.value(),self.K_max_4.value()],[self.P_min_4.value(),self.P_max_4.value()], [self.e_min_4.value(),self.e_max_4.value()],[self.om_min_4.value(),self.om_max_4.value()], [self.ma_min_4.value(),self.ma_max_4.value()],[self.incl_min_4.value(),self.incl_max_4.value()], [self.Omega_min_4.value(),self.Omega_max_4.value()],[self.t0_min_4.value(),self.t0_max_4.value()],[self.pl_rad_min_4.value(),self.pl_rad_max_4.value()],[self.a_sol_min_4.value(),self.a_sol_max_4.value()],
        [self.K_min_5.value(),self.K_max_5.value()],[self.P_min_5.value(),self.P_max_5.value()], [self.e_min_5.value(),self.e_max_5.value()],[self.om_min_5.value(),self.om_max_5.value()], [self.ma_min_5.value(),self.ma_max_5.value()],[self.incl_min_5.value(),self.incl_max_5.value()], [self.Omega_min_5.value(),self.Omega_max_5.value()],[self.t0_min_5.value(),self.t0_max_5.value()],[self.pl_rad_min_5.value(),self.pl_rad_max_5.value()],[self.a_sol_min_5.value(),self.a_sol_max_5.value()],
        [self.K_min_6.value(),self.K_max_6.value()],[self.P_min_6.value(),self.P_max_6.value()], [self.e_min_6.value(),self.e_max_6.value()],[self.om_min_6.value(),self.om_max_6.value()], [self.ma_min_6.value(),self.ma_max_6.value()],[self.incl_min_6.value(),self.incl_max_6.value()], [self.Omega_min_6.value(),self.Omega_max_6.value()],[self.t0_min_6.value(),self.t0_max_6.value()],[self.pl_rad_min_6.value(),self.pl_rad_max_6.value()],[self.a_sol_min_6.value(),self.a_sol_max_6.value()],
        [self.K_min_7.value(),self.K_max_7.value()],[self.P_min_7.value(),self.P_max_7.value()], [self.e_min_7.value(),self.e_max_7.value()],[self.om_min_7.value(),self.om_max_7.value()], [self.ma_min_7.value(),self.ma_max_7.value()],[self.incl_min_7.value(),self.incl_max_7.value()], [self.Omega_min_7.value(),self.Omega_max_7.value()],[self.t0_min_7.value(),self.t0_max_7.value()],[self.pl_rad_min_7.value(),self.pl_rad_max_7.value()],[self.a_sol_min_7.value(),self.a_sol_max_7.value()],
        [self.K_min_8.value(),self.K_max_8.value()],[self.P_min_8.value(),self.P_max_8.value()], [self.e_min_8.value(),self.e_max_8.value()],[self.om_min_8.value(),self.om_max_8.value()], [self.ma_min_8.value(),self.ma_max_8.value()],[self.incl_min_8.value(),self.incl_max_8.value()], [self.Omega_min_8.value(),self.Omega_max_8.value()],[self.t0_min_8.value(),self.t0_max_8.value()],[self.pl_rad_min_8.value(),self.pl_rad_max_8.value()],[self.a_sol_min_8.value(),self.a_sol_max_8.value()],
        [self.K_min_9.value(),self.K_max_9.value()],[self.P_min_9.value(),self.P_max_9.value()], [self.e_min_9.value(),self.e_max_9.value()],[self.om_min_9.value(),self.om_max_9.value()], [self.ma_min_9.value(),self.ma_max_9.value()],[self.incl_min_9.value(),self.incl_max_9.value()], [self.Omega_min_9.value(),self.Omega_max_9.value()],[self.t0_min_9.value(),self.t0_max_9.value()],[self.pl_rad_min_9.value(),self.pl_rad_max_9.value()],[self.a_sol_min_9.value(),self.a_sol_max_9.value()]               
        ]
 
        for i in range(fit.npl):
            fit.K_bound[i] = param_bounds_gui[10*i + 0]    
            fit.P_bound[i] = param_bounds_gui[10*i + 1]    
            fit.e_bound[i] = param_bounds_gui[10*i + 2]    
            fit.w_bound[i] = param_bounds_gui[10*i + 3]    
            fit.M0_bound[i] = param_bounds_gui[10*i + 4]    
            fit.i_bound[i] = param_bounds_gui[10*i + 5]    
            fit.Node_bound[i] = param_bounds_gui[10*i + 6]    
            fit.t0_bound[i]  =  param_bounds_gui[10*i + 7]
            fit.pl_rad_bound[i]  =   param_bounds_gui[10*i + 8]
            fit.pl_a_bound[i]   =   param_bounds_gui[10*i + 9]

        offset_bounds_gui = [
        [self.Data1_min.value(),self.Data1_max.value()], [self.Data2_min.value(),self.Data2_max.value()], [self.Data3_min.value(),self.Data3_max.value()], [self.Data4_min.value(),self.Data4_max.value()], [self.Data5_min.value(),self.Data5_max.value()],   
        [self.Data6_min.value(),self.Data6_max.value()], [self.Data7_min.value(),self.Data7_max.value()], [self.Data8_min.value(),self.Data8_max.value()], [self.Data9_min.value(),self.Data9_max.value()], [self.Data10_min.value(),self.Data10_max.value()]
        ]
        
        jitter_bounds_gui = [
        [self.jitter1_min.value(),self.jitter1_max.value()], [self.jitter2_min.value(),self.jitter2_max.value()], [self.jitter3_min.value(),self.jitter3_max.value()], [self.jitter4_min.value(),self.jitter4_max.value()], [self.jitter5_min.value(),self.jitter5_max.value()],   
        [self.jitter6_min.value(),self.jitter6_max.value()], [self.jitter7_min.value(),self.jitter7_max.value()], [self.jitter8_min.value(),self.jitter8_max.value()], [self.jitter9_min.value(),self.jitter9_max.value()], [self.jitter10_min.value(),self.Data10_max.value()]   
        ]  
    
    
        for i in range(10): 
            fit.rvoff_bounds[i] = offset_bounds_gui[i]
            fit.jitt_bounds[i]  = jitter_bounds_gui[i] 
    
 
        fit.rv_lintr_bounds[0]  = [self.lin_trend_min.value(),self.lin_trend_max.value()]
        #self.st_mass_bounds  = {k: np.array([0.01,100]) for k in range(1)} 

        GP_rot_bounds_gui = [
        [self.GP_rot_kernel_Amp_min.value(),self.GP_rot_kernel_Amp_max.value()],  
        [self.GP_rot_kernel_time_sc_min.value(),self.GP_rot_kernel_time_sc_max.value()],  
        [self.GP_rot_kernel_Per_min.value(),self.GP_rot_kernel_Per_max.value()],  
        [self.GP_rot_kernel_fact_min.value(),self.GP_rot_kernel_fact_max.value()],  
        ]
 
        for i in range(4): 
            fit.GP_rot_bounds[i] = GP_rot_bounds_gui[i]
            
        GP_sho_bounds_gui = [
        [self.GP_sho_kernel_S_min.value(),self.GP_sho_kernel_S_max.value()],  
        [self.GP_sho_kernel_Q_min.value(),self.GP_sho_kernel_Q_max.value()],  
        [self.GP_sho_kernel_omega_min.value(),self.GP_sho_kernel_omega_max.value()],  
        ]
 
        for i in range(3): 
            fit.GP_sho_bounds[i] = GP_sho_bounds_gui[i]            
            
            
            
            
    def check_priors(self):
        global fit

        
        
        param_nr_priors_gui = [
        [self.K_mean_1.value(),self.K_sigma_1.value(),self.use_K_norm_pr_1.isChecked()],[self.P_mean_1.value(),self.P_sigma_1.value(),self.use_P_norm_pr_1.isChecked()], [self.e_mean_1.value(),self.e_sigma_1.value(),self.use_e_norm_pr_1.isChecked()],[self.om_mean_1.value(),self.om_sigma_1.value(),self.use_om_norm_pr_1.isChecked()], [self.ma_mean_1.value(),self.ma_sigma_1.value(),self.use_ma_norm_pr_1.isChecked()],[self.incl_mean_1.value(),self.incl_sigma_1.value(),self.use_incl_norm_pr_1.isChecked()], [self.Omega_mean_1.value(),self.Omega_sigma_1.value(), self.use_Omega_norm_pr_1.isChecked()],[self.t0_mean_1.value(),self.t0_sigma_1.value(), self.use_t0_norm_pr_1.isChecked()],[self.pl_rad_mean_1.value(),self.pl_rad_sigma_1.value(),self.use_pl_rad_norm_pr_1.isChecked()],[self.a_sol_mean_1.value(),self.a_sol_sigma_1.value(),self.use_a_sol_norm_pr_1.isChecked()],
        [self.K_mean_2.value(),self.K_sigma_2.value(),self.use_K_norm_pr_2.isChecked()],[self.P_mean_2.value(),self.P_sigma_2.value(),self.use_P_norm_pr_2.isChecked()], [self.e_mean_2.value(),self.e_sigma_2.value(),self.use_e_norm_pr_2.isChecked()],[self.om_mean_2.value(),self.om_sigma_2.value(),self.use_om_norm_pr_2.isChecked()], [self.ma_mean_2.value(),self.ma_sigma_2.value(),self.use_ma_norm_pr_2.isChecked()],[self.incl_mean_2.value(),self.incl_sigma_2.value(),self.use_incl_norm_pr_2.isChecked()], [self.Omega_mean_2.value(),self.Omega_sigma_2.value(), self.use_Omega_norm_pr_2.isChecked()],[self.t0_mean_2.value(),self.t0_sigma_2.value(), self.use_t0_norm_pr_2.isChecked()],[self.pl_rad_mean_2.value(),self.pl_rad_sigma_2.value(),self.use_pl_rad_norm_pr_2.isChecked()],[self.a_sol_mean_2.value(),self.a_sol_sigma_2.value(),self.use_a_sol_norm_pr_2.isChecked()],
        [self.K_mean_3.value(),self.K_sigma_3.value(),self.use_K_norm_pr_3.isChecked()],[self.P_mean_3.value(),self.P_sigma_3.value(),self.use_P_norm_pr_3.isChecked()], [self.e_mean_3.value(),self.e_sigma_3.value(),self.use_e_norm_pr_3.isChecked()],[self.om_mean_3.value(),self.om_sigma_3.value(),self.use_om_norm_pr_3.isChecked()], [self.ma_mean_3.value(),self.ma_sigma_3.value(),self.use_ma_norm_pr_3.isChecked()],[self.incl_mean_3.value(),self.incl_sigma_3.value(),self.use_incl_norm_pr_3.isChecked()], [self.Omega_mean_3.value(),self.Omega_sigma_3.value(), self.use_Omega_norm_pr_3.isChecked()],[self.t0_mean_3.value(),self.t0_sigma_3.value(), self.use_t0_norm_pr_3.isChecked()],[self.pl_rad_mean_3.value(),self.pl_rad_sigma_3.value(),self.use_pl_rad_norm_pr_3.isChecked()],[self.a_sol_mean_3.value(),self.a_sol_sigma_3.value(),self.use_a_sol_norm_pr_3.isChecked()],
        [self.K_mean_4.value(),self.K_sigma_4.value(),self.use_K_norm_pr_4.isChecked()],[self.P_mean_4.value(),self.P_sigma_4.value(),self.use_P_norm_pr_4.isChecked()], [self.e_mean_4.value(),self.e_sigma_4.value(),self.use_e_norm_pr_4.isChecked()],[self.om_mean_4.value(),self.om_sigma_4.value(),self.use_om_norm_pr_4.isChecked()], [self.ma_mean_4.value(),self.ma_sigma_4.value(),self.use_ma_norm_pr_4.isChecked()],[self.incl_mean_4.value(),self.incl_sigma_4.value(),self.use_incl_norm_pr_4.isChecked()], [self.Omega_mean_4.value(),self.Omega_sigma_4.value(), self.use_Omega_norm_pr_4.isChecked()],[self.t0_mean_4.value(),self.t0_sigma_4.value(), self.use_t0_norm_pr_4.isChecked()],[self.pl_rad_mean_4.value(),self.pl_rad_sigma_4.value(),self.use_pl_rad_norm_pr_4.isChecked()],[self.a_sol_mean_4.value(),self.a_sol_sigma_4.value(),self.use_a_sol_norm_pr_4.isChecked()],
        [self.K_mean_5.value(),self.K_sigma_5.value(),self.use_K_norm_pr_5.isChecked()],[self.P_mean_5.value(),self.P_sigma_5.value(),self.use_P_norm_pr_5.isChecked()], [self.e_mean_5.value(),self.e_sigma_5.value(),self.use_e_norm_pr_5.isChecked()],[self.om_mean_5.value(),self.om_sigma_5.value(),self.use_om_norm_pr_5.isChecked()], [self.ma_mean_5.value(),self.ma_sigma_5.value(),self.use_ma_norm_pr_5.isChecked()],[self.incl_mean_5.value(),self.incl_sigma_5.value(),self.use_incl_norm_pr_5.isChecked()], [self.Omega_mean_5.value(),self.Omega_sigma_5.value(), self.use_Omega_norm_pr_5.isChecked()],[self.t0_mean_5.value(),self.t0_sigma_5.value(), self.use_t0_norm_pr_5.isChecked()],[self.pl_rad_mean_5.value(),self.pl_rad_sigma_5.value(),self.use_pl_rad_norm_pr_5.isChecked()],[self.a_sol_mean_5.value(),self.a_sol_sigma_5.value(),self.use_a_sol_norm_pr_5.isChecked()],
        [self.K_mean_6.value(),self.K_sigma_6.value(),self.use_K_norm_pr_6.isChecked()],[self.P_mean_6.value(),self.P_sigma_6.value(),self.use_P_norm_pr_6.isChecked()], [self.e_mean_6.value(),self.e_sigma_6.value(),self.use_e_norm_pr_6.isChecked()],[self.om_mean_6.value(),self.om_sigma_6.value(),self.use_om_norm_pr_6.isChecked()], [self.ma_mean_6.value(),self.ma_sigma_6.value(),self.use_ma_norm_pr_6.isChecked()],[self.incl_mean_6.value(),self.incl_sigma_6.value(),self.use_incl_norm_pr_6.isChecked()], [self.Omega_mean_6.value(),self.Omega_sigma_6.value(), self.use_Omega_norm_pr_6.isChecked()],[self.t0_mean_6.value(),self.t0_sigma_6.value(), self.use_t0_norm_pr_6.isChecked()],[self.pl_rad_mean_6.value(),self.pl_rad_sigma_6.value(),self.use_pl_rad_norm_pr_6.isChecked()],[self.a_sol_mean_6.value(),self.a_sol_sigma_6.value(),self.use_a_sol_norm_pr_6.isChecked()],
        [self.K_mean_7.value(),self.K_sigma_7.value(),self.use_K_norm_pr_7.isChecked()],[self.P_mean_7.value(),self.P_sigma_7.value(),self.use_P_norm_pr_7.isChecked()], [self.e_mean_7.value(),self.e_sigma_7.value(),self.use_e_norm_pr_7.isChecked()],[self.om_mean_7.value(),self.om_sigma_7.value(),self.use_om_norm_pr_7.isChecked()], [self.ma_mean_7.value(),self.ma_sigma_7.value(),self.use_ma_norm_pr_7.isChecked()],[self.incl_mean_7.value(),self.incl_sigma_7.value(),self.use_incl_norm_pr_7.isChecked()], [self.Omega_mean_7.value(),self.Omega_sigma_7.value(), self.use_Omega_norm_pr_7.isChecked()],[self.t0_mean_7.value(),self.t0_sigma_7.value(), self.use_t0_norm_pr_7.isChecked()],[self.pl_rad_mean_7.value(),self.pl_rad_sigma_7.value(),self.use_pl_rad_norm_pr_7.isChecked()],[self.a_sol_mean_7.value(),self.a_sol_sigma_7.value(),self.use_a_sol_norm_pr_7.isChecked()],
        [self.K_mean_8.value(),self.K_sigma_8.value(),self.use_K_norm_pr_8.isChecked()],[self.P_mean_8.value(),self.P_sigma_8.value(),self.use_P_norm_pr_8.isChecked()], [self.e_mean_8.value(),self.e_sigma_8.value(),self.use_e_norm_pr_8.isChecked()],[self.om_mean_8.value(),self.om_sigma_8.value(),self.use_om_norm_pr_8.isChecked()], [self.ma_mean_8.value(),self.ma_sigma_8.value(),self.use_ma_norm_pr_8.isChecked()],[self.incl_mean_8.value(),self.incl_sigma_8.value(),self.use_incl_norm_pr_8.isChecked()], [self.Omega_mean_8.value(),self.Omega_sigma_8.value(), self.use_Omega_norm_pr_8.isChecked()],[self.t0_mean_8.value(),self.t0_sigma_8.value(), self.use_t0_norm_pr_8.isChecked()],[self.pl_rad_mean_8.value(),self.pl_rad_sigma_8.value(),self.use_pl_rad_norm_pr_8.isChecked()],[self.a_sol_mean_8.value(),self.a_sol_sigma_8.value(),self.use_a_sol_norm_pr_8.isChecked()],
        [self.K_mean_9.value(),self.K_sigma_9.value(),self.use_K_norm_pr_9.isChecked()],[self.P_mean_9.value(),self.P_sigma_9.value(),self.use_P_norm_pr_9.isChecked()], [self.e_mean_9.value(),self.e_sigma_9.value(),self.use_e_norm_pr_9.isChecked()],[self.om_mean_9.value(),self.om_sigma_9.value(),self.use_om_norm_pr_9.isChecked()], [self.ma_mean_9.value(),self.ma_sigma_9.value(),self.use_ma_norm_pr_9.isChecked()],[self.incl_mean_9.value(),self.incl_sigma_9.value(),self.use_incl_norm_pr_9.isChecked()], [self.Omega_mean_9.value(),self.Omega_sigma_9.value(), self.use_Omega_norm_pr_9.isChecked()],[self.t0_mean_9.value(),self.t0_sigma_9.value(), self.use_t0_norm_pr_9.isChecked()],[self.pl_rad_mean_9.value(),self.pl_rad_sigma_9.value(),self.use_pl_rad_norm_pr_9.isChecked()],[self.a_sol_mean_9.value(),self.a_sol_sigma_9.value(),self.use_a_sol_norm_pr_9.isChecked()],
        ]
 
        for i in range(fit.npl):
            fit.K_norm_pr[i]  = param_nr_priors_gui[10*i + 0]    
            fit.P_norm_pr[i]  = param_nr_priors_gui[10*i + 1]    
            fit.e_norm_pr[i]  = param_nr_priors_gui[10*i + 2]    
            fit.w_norm_pr[i]  = param_nr_priors_gui[10*i + 3]    
            fit.M0_norm_pr[i] = param_nr_priors_gui[10*i + 4]    
            fit.i_norm_pr[i]  = param_nr_priors_gui[10*i + 5]    
            fit.Node_norm_pr[i] = param_nr_priors_gui[10*i + 6]    
            fit.t0_norm_pr[i]   = param_nr_priors_gui[10*i + 7]
            fit.pl_rad_norm_pr[i]  = param_nr_priors_gui[10*i + 8]
            fit.pl_a_norm_pr[i]    = param_nr_priors_gui[10*i + 9]

       # offset_nr_priors_gui = [
      #  [self.Data1_mean.value(),self.Data1_sigma.value()], [self.Data2_mean.value(),self.Data2_sigma.value()], [self.Data3_mean.value(),self.Data3_sigma.value()], [self.Data4_mean.value(),self.Data4_sigma.value()], [self.Data5_mean.value(),self.Data5_sigma.value()],   
      #  [self.Data6_mean.value(),self.Data6_sigma.value()], [self.Data7_mean.value(),self.Data7_sigma.value()], [self.Data8_mean.value(),self.Data8_sigma.value()], [self.Data9_mean.value(),self.Data9_sigma.value()], [self.Data10_mean.value(),self.Data10_sigma.value()]
      #  ]
        
       # jitter_nr_priors_gui = [
      #  [self.jitter1_mean.value(),self.jitter1_sigma.value()], [self.jitter2_mean.value(),self.jitter2_sigma.value()], [self.jitter3_mean.value(),self.jitter3_sigma.value()], [self.jitter4_mean.value(),self.jitter4_sigma.value()], [self.jitter5_mean.value(),self.jitter5_sigma.value()],   
      #  [self.jitter6_mean.value(),self.jitter6_sigma.value()], [self.jitter7_mean.value(),self.jitter7_sigma.value()], [self.jitter8_mean.value(),self.jitter8_sigma.value()], [self.jitter9_mean.value(),self.jitter9_sigma.value()], [self.jitter10_mean.value(),self.Data10_sigma.value()]   
      #  ]  
    
    
       # for i in range(10): 
       #     fit.rvoff_norm_pr[i] = offset_nr_priors_gui[i]
         #   fit.jitt_norm_pr[i]  = jitter_nr_priors_gui[i] 
    
 
       # fit.rv_lintr_norm_pr[0]  = [self.lin_trend_mean.value(),self.lin_trend_sigma.value()]
        #self.st_mass_bounds  = {k: np.array([0.01,100]) for k in range(1)} 

        GP_rot_nr_priors_gui = [
        [self.GP_rot_kernel_Amp_mean.value(),self.GP_rot_kernel_Amp_sigma.value(),self.use_GP_rot_kernel_Amp_nr_pr.isChecked()],  
        [self.GP_rot_kernel_time_sc_mean.value(),self.GP_rot_kernel_time_sc_sigma.value(),self.use_GP_rot_kernel_time_sc_nr_pr.isChecked()],  
        [self.GP_rot_kernel_Per_mean.value(),self.GP_rot_kernel_Per_sigma.value(),self.use_GP_rot_kernel_Per_sigma_nr_pr.isChecked()],  
        [self.GP_rot_kernel_fact_mean.value(),self.GP_rot_kernel_fact_sigma.value(),self.use_GP_rot_kernel_fact_nr_pr.isChecked()],  
        ]
 
        for i in range(4): 
            fit.GP_rot_norm_pr[i] = GP_rot_nr_priors_gui[i]            
    

        GP_sho_nr_priors_gui = [
        [self.GP_sho_kernel_S_mean.value(),self.GP_sho_kernel_S_sigma.value(), self.use_GP_sho_kernel_S_nr_pr.isChecked()],  
        [self.GP_sho_kernel_Q_mean.value(),self.GP_sho_kernel_Q_sigma.value(), self.use_GP_sho_kernel_Q_nr_pr.isChecked()],  
        [self.GP_sho_kernel_omega_mean.value(),self.GP_sho_kernel_omega_sigma.value(), self.use_GP_sho_kernel_omega_nr_pr.isChecked()],  
        ]
 
        for i in range(3): 
            fit.GP_sho_norm_pr[i] = GP_sho_nr_priors_gui[i]   


    
####################################################        
  
    def initialize_buttons(self):

        # for some reason this does not work!
        #[self.buttonGroup_4.setId(bg4, ii) for ii, bg4 in enumerate(self.buttonGroup_4.buttons())]
        #[self.buttonGroup_remove_RV_data.setId(bg5, jj) for jj, bg5 in enumerate(self.buttonGroup_remove_RV_data.buttons())]   
        
        self.buttonGroup_4.setId(self.Button_RV_data_1,1)
        self.buttonGroup_4.setId(self.Button_RV_data_2,2)
        self.buttonGroup_4.setId(self.Button_RV_data_3,3)
        self.buttonGroup_4.setId(self.Button_RV_data_4,4)
        self.buttonGroup_4.setId(self.Button_RV_data_5,5)
        self.buttonGroup_4.setId(self.Button_RV_data_6,6)
        self.buttonGroup_4.setId(self.Button_RV_data_7,7)
        self.buttonGroup_4.setId(self.Button_RV_data_8,8)
        self.buttonGroup_4.setId(self.Button_RV_data_9,9)
        self.buttonGroup_4.setId(self.Button_RV_data_10,10)

        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data1,1)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data2,2)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data3,3)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data4,4)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data5,5)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data6,6)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data7,7)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data8,8)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data9,9)
        self.buttonGroup_remove_RV_data.setId(self.remove_rv_data10,10)
             
        self.buttonGroup_transit_data.setId(self.Button_transit_data_1,1)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_2,2)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_3,3)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_4,4)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_5,5)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_6,6)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_7,7)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_8,8)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_9,9)
        self.buttonGroup_transit_data.setId(self.Button_transit_data_10,10)

        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data1,1)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data2,2)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data3,3)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data4,4)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data5,5)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data6,6)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data7,7)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data8,8)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data9,9)
        self.buttonGroup_remove_transit_data.setId(self.remove_transit_data10,10)

        self.buttonGroup_activity_data.setId(self.Button_activity_data_1,1)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_2,2)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_3,3)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_4,4)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_5,5)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_6,6)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_7,7)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_8,8)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_9,9)
        self.buttonGroup_activity_data.setId(self.Button_activity_data_10,10)

        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data1,1)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data2,2)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data3,3)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data4,4)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data5,5)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data6,6)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data7,7)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data8,8)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data9,9)
        self.buttonGroup_remove_activity_data.setId(self.remove_activity_data10,10)       
        
        self.buttonGroup_color_picker.setId(self.pushButton_color_1,1)
        self.buttonGroup_color_picker.setId(self.pushButton_color_2,2)
        self.buttonGroup_color_picker.setId(self.pushButton_color_3,3)
        self.buttonGroup_color_picker.setId(self.pushButton_color_4,4)
        self.buttonGroup_color_picker.setId(self.pushButton_color_5,5)
        self.buttonGroup_color_picker.setId(self.pushButton_color_6,6)
        self.buttonGroup_color_picker.setId(self.pushButton_color_7,7)
        self.buttonGroup_color_picker.setId(self.pushButton_color_8,8)
        self.buttonGroup_color_picker.setId(self.pushButton_color_9,9)
        self.buttonGroup_color_picker.setId(self.pushButton_color_10,10)
        
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_1,1)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_2,2)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_3,3)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_4,4)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_5,5)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_6,6)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_7,7)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_8,8)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_9,9)
        self.buttonGroup_symbol_picker.setId(self.pushButton_symbol_10,10)        
        
        
      
        
    def initialize_plots(self):

        global p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,pe,pdi

        p1  = self.graphicsView_timeseries_RV
        p2  = self.graphicsView_timeseries_RV_o_c
        p3  = self.graphicsView_timeseries_phot
        p4  = self.graphicsView_timeseries_phot_o_c
        p5  = self.graphicsView_timeseries_activity
        p6  = self.graphicsView_timeseries_correlations
                
        p7  = self.graphicsView_peridogram_RV 
        p8  = self.graphicsView_periodogram_RV_o_c  
        p9  = self.graphicsView_peridogram_phot
        p10 = self.graphicsView_peridogram_phot_o_c        
        p11 = self.graphicsView_periodogram_activity
        p12 = self.graphicsView_periodogram_window  
        
        p13 = self.graphicsView_orb_evol_elements_a
        p14 = self.graphicsView_orb_evol_elements_e        
        p15 = self.graphicsView_orbital_view
        
        pe  = self.graphicsView_extra_plot
        
        pdi = self.load_data_plot

        xaxis = ['BJD','BJD','BJD','BJD','BJD','x','days','days','days','days','days','days','yrs','yrs','a','','x']
        yaxis = ['RV','RV','Relative Flux','Relative Flux','y','y','power','power','SDE','SDE','power','power','a','e','a','','y']       
        xunit = ['d' ,'d','d','d','d','','','','','','','','','','au','','']
        yunit = ['m/s' ,'m/s' , '','','','','','','','','','','','','au','','']

        zzz = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,pe,pdi]
        font=QtGui.QFont()
        font.setPixelSize(12) 
        for i in range(len(zzz)):
 

                zzz[i].getAxis("bottom").tickFont = font
                zzz[i].getAxis("bottom").setStyle(tickTextOffset = 12)
                zzz[i].getAxis("top").tickFont = font
                zzz[i].getAxis("top").setStyle(tickTextOffset = 12)
                zzz[i].getAxis("left").tickFont = font
                zzz[i].getAxis("left").setStyle(tickTextOffset = 12)
                zzz[i].getAxis("right").tickFont = font
                zzz[i].getAxis("right").setStyle(tickTextOffset = 12)
                zzz[i].getAxis('left').setWidth(50)
                zzz[i].getAxis('right').setWidth(10)
                zzz[i].getAxis('top').setHeight(10)
                zzz[i].getAxis('bottom').setHeight(50)
                            
                zzz[i].setLabel('bottom', '%s'%xaxis[i], units='%s'%xunit[i],  **{'font-size':'12pt'})
                zzz[i].setLabel('left',   '%s'%yaxis[i], units='%s'%yunit[i],  **{'font-size':'12pt'})       
                zzz[i].showAxis('top') 
                zzz[i].showAxis('right') 
                zzz[i].getAxis('bottom').enableAutoSIPrefix(enable=False)

        p15.getViewBox().setAspectLocked(True)

        return   
        

        
    def identify_power_peaks(self,x,y,sig_level=np.array([]), power_level=np.array([])):
 
        per_ind = argrelextrema(y, np.greater)
        per_x   = x[per_ind]
        per_y   = y[per_ind]     

        peaks_sort = sorted(range(len(per_y)), key=lambda k: per_y[k], reverse=True)

        per_x   = per_x[peaks_sort]   
        per_y   = per_y[peaks_sort]  
        
        ################## text generator #################
        text_peaks = """ 
"""
        if power_level.size != 0 and sig_level.size != 0:
         
            text_peaks = text_peaks +"""FAP levels
-----------------------------------  
"""        
            for ii in range(len(power_level)):     
                text_peaks = text_peaks +"""
%.2f per cent = %.4f"""%(power_level[ii]*100.0,sig_level[ii])       
        
        text_peaks = text_peaks + """
----------------------------------------------
The 10 strongest peaks
----------------------------------------------
"""         
        for j in range(10):
            text_peaks = text_peaks +"""
period = %.2f [d], power = %.4f"""%(per_x[j],per_y[j])  
            if sig_level.size != 0 and per_y[j] > sig_level[-1]:
                text_peaks = text_peaks +"""  significant"""
                
        ################################################        
    
        return text_peaks  
        
  
    
        
######################## Correlation plots ###################################### 
        
    def init_correlations_combo(self):
        global fit
        self.comboBox_corr_1.clear()
        self.comboBox_corr_2.clear()
        
        self.initialize_corr_y = {k: [] for k in range(20)}
        z = 0 

        if fit.filelist.ndset != 0:

            for i in range(max(fit.filelist.idset)+1):
                self.comboBox_corr_1.addItem('RV %s'%(i+1),i+1) 
                self.comboBox_corr_2.addItem('RV %s'%(i+1),i+1) 
            
                self.initialize_corr_y[z] = np.array([fit.fit_results.rv_model.jd[fit.filelist.idset==i],
                                                      fit.fit_results.rv_model.rvs[fit.filelist.idset==i], 
                                                      fit.fit_results.rv_model.rv_err[fit.filelist.idset==i]])  
                z +=1
                
            for i in range(max(fit.filelist.idset)+1):
                self.comboBox_corr_1.addItem('RV o-c %s'%(i+1),i+1)         
                self.comboBox_corr_2.addItem('RV o-c %s'%(i+1),i+1)  
    
                self.initialize_corr_y[z] = np.array([fit.fit_results.rv_model.jd[fit.filelist.idset==i],
                                                      fit.fit_results.rv_model.o_c[fit.filelist.idset==i], 
                                                      fit.fit_results.rv_model.rv_err[fit.filelist.idset==i]]) 
                z +=1                          
         

        for i in range(0,10,1):         
            if len(fit.act_data_sets[i]) != 0: 
                self.comboBox_corr_1.addItem('act. data %s'%(i+1),i+1)       
                self.comboBox_corr_2.addItem('act. data %s'%(i+1),i+1) 
                
                self.initialize_corr_y[z] = fit.act_data_sets[i] 
                z +=1                                         
                
        #return                
                
                
    def update_correlations_data_plots(self):
        global fit, colors,  p6 
        
        ind1 = self.comboBox_corr_1.currentIndex()
        ind2 = self.comboBox_corr_2.currentIndex()
 
        p6.plot(clear=True,)  
        
        self.color_corr.setStyleSheet("color: %s;"%colors[0]) 

        #p6.autoRange()     
        
        if not ind1 == None and not ind2 == None:


            #err1 = pg.ErrorBarItem(x=fit.act_data_sets[ind][0], y=fit.act_data_sets[ind][1],symbol='o', 
            #height=fit.act_data_sets[ind][2], beam=0.0, pen=fit.colors[ind])  

            #p6.addItem(err1)      
            #p6.addLine(x=None, y=0, pen=pg.mkPen('#ff9933', width=0.8))
            
            
            if len(self.initialize_corr_y[ind1][0]) == len(self.initialize_corr_y[ind2][0]):
                p6.plot(self.initialize_corr_y[ind1][1],self.initialize_corr_y[ind2][1], pen=None,symbol='o',
                #symbolPen=,
                symbolSize=self.act_data_size.value(),enableAutoRange=True,viewRect=True,
                symbolBrush=colors[0]
                )    
                
                
                pears = pearsonr(self.initialize_corr_y[ind1][1],self.initialize_corr_y[ind2][1] )
                
                if pears[0] < 0:
                    pos_neg = "negative"
                else:
                    pos_neg = "positive"
                    
                if abs(pears[0]) < 0.3:                      
                    strong_mod_weak = "very weak"
                elif 0.3 <= abs(pears[0]) <= 0.5: 
                     strong_mod_weak = "weak"
                elif 0.5 <= abs(pears[0]) <= 0.7: 
                     strong_mod_weak = "moderate"                       
                elif 0.7 <= abs(pears[0]) <= 1: 
                     strong_mod_weak = "strong"  
                else:
                     strong_mod_weak = "n/a"  
                     
                m, c = np.polyfit(self.initialize_corr_y[ind1][1],self.initialize_corr_y[ind2][1], 1,
                                  w=1/np.sqrt(self.initialize_corr_y[ind1][2]**2 + self.initialize_corr_y[ind2][2]**2),
                                  full=False,cov=True)  
                
                e = np.sqrt(np.diag(c))
                
                text = '''Pearson's correlation coefficient 2-tailed p-value: 
%s, %s
(A %s %s correlation)

Polyfit coefficients: 
%s +/- %s, 
%s +/- %s   

'''%(pears[0],pears[1], pos_neg, strong_mod_weak, m[0],e[0], m[1],e[1])

                self.corr_print_info.clicked.connect(lambda: self.print_info_for_object(text))

                #self.console_widget.print_text(text)
                #print(text)
                
                if self.plot_corr_err.isChecked():
                    err1 = pg.ErrorBarItem(x=self.initialize_corr_y[ind1][1], y=self.initialize_corr_y[ind2][1],symbol='o', 
                    top=self.initialize_corr_y[ind2][2],bottom=self.initialize_corr_y[ind2][2], 
                    left=self.initialize_corr_y[ind1][2],right=self.initialize_corr_y[ind1][2],                     
                    beam=0.0, pen=colors[0])  

                    p6.addItem(err1)   
                    
                if self.plot_corr_coef.isChecked():

                    p6.plot(self.initialize_corr_y[ind1][1], self.initialize_corr_y[ind1][1]*m[0] +m[1] , pen='k')                            
 
                    #p6.addItem(trend)                      
                    

                
                p6.autoRange()
            

                return   
            
            else:               
                text_err = pg.TextItem('Not the same time series!',color=(0,0,0))#, anchor=(0,0), border='w',color) #, fill=(0, 0, 255, 100))
                p6.addItem(text_err, ignoreBounds=True)   
        else:   
             
                return

    def get_corr_color(self):
        global fit
        
        colorz = QtGui.QColorDialog.getColor()
        colors[0]=colorz.name()   

        self.update_correlations_data_plots()

    def corr_plot_x_labels(self):
        global fit
        
        text, okPressed = QtGui.QInputDialog.getText(self, "x-axis label","(No special characters!)", QtGui.QLineEdit.Normal, "")
        
        if okPressed and text != '':
            p6.setLabel('bottom', '%s'%text, units='',  **{'font-size':'11pt'})
 
        else:
            return
    
        self.update_correlations_data_plots()
 

    def corr_plot_y_labels(self):
        global fit
        
        text, okPressed = QtGui.QInputDialog.getText(self, "y-axis label","(No special characters!)", QtGui.QLineEdit.Normal, "")
        
        if okPressed and text != '':
            p6.setLabel('left', '%s'%text, units='',  **{'font-size':'11pt'})
 
        else:
            return
    
        self.update_correlations_data_plots()
              
        
        
######################## Activity plots ######################################  
                
    def init_activity_combo(self):
        global fit
        
        for i in range(10):
            self.comboBox_act_data_gls.addItem('act. data %s'%(i+1),i+1)       
            self.comboBox_act_data.addItem('act. data %s'%(i+1),i+1)       
                
        #self.comboBox_act_data_gls.activated.connect(self.handleActivated_act_gls) 
        
   # def handleActivated_act_gls(self, index):
   #     global fit 
    
   #     ind = self.comboBox_act_data_gls.itemData(index)         
   #     self.update_activity_gls_plots(ind-1)
        
        
        
 
    def update_activity_gls_plots(self,ind):
        global fit, colors,  p11 
 
        omega = 1/ np.logspace(np.log(self.gls_min_period.value()), np.log(self.gls_max_period.value()), num=self.gls_n_omega.value())
        power_levels = np.array([self.gls_fap1.value(),self.gls_fap2.value(),self.gls_fap3.value()])
  
        if len(fit.act_data_sets[ind]) != 0 and len(fit.act_data_sets[ind][0]) > 5:

            p11.plot(clear=True,)        
 
            act_per = gls.Gls((fit.act_data_sets[ind][0], fit.act_data_sets[ind][1],fit.act_data_sets[ind][2]), 
            fast=True,  verbose=False, norm= "ZK",ofac=self.gls_ofac.value(), fbeg=omega[-1], fend=omega[ 0],)
            
            ######################## GLS ##############################
            if self.radioButton_act_GLS_period.isChecked():
                p11.setLogMode(True,False)        
                p11.plot(1/act_per.freq, act_per.power,pen=fit.colors[ind],symbol=None ) 
                p11.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'}) 

            else:
                p11.setLogMode(False,False)        
                p11.plot(act_per.freq, act_per.power,pen=fit.colors[ind],symbol=None )                    
                p11.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'}) 

                                               
            [p11.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(act_per.powerLevel(np.array(power_levels)))]
  
            self.act_periodogram_print_info.clicked.connect(lambda: self.print_info_for_object(
            act_per.info(stdout=False) + 
            self.identify_power_peaks(1/act_per.freq, act_per.power, power_level = power_levels, sig_level = act_per.powerLevel(np.array(power_levels)) )))   
    
            return
        else:   
            p11.plot(clear=True,)        

            return



    def update_activity_data_plots(self,ind):
        global fit, colors,  p5 

        if len(fit.act_data_sets[ind]) != 0:

            p5.plot(clear=True,)  

            err1 = pg.ErrorBarItem(x=fit.act_data_sets[ind][0], y=fit.act_data_sets[ind][1],symbol='o', 
            height=fit.act_data_sets[ind][2], beam=0.0, pen=fit.colors[ind])  

            p5.addItem(err1)      
            p5.addLine(x=None, y=0, pen=pg.mkPen('#ff9933', width=0.8))

            p5.plot(fit.act_data_sets[ind][0],fit.act_data_sets[ind][1], pen=None,symbol='o',
            #symbolPen=,
            symbolSize=self.act_data_size.value(),enableAutoRange=True,viewRect=True,
            symbolBrush=fit.colors[ind]            
            )      

            p5.setLabel('left', 'y', units='',  **{'font-size':'11pt'})     

            return
        else:   
            p5.plot(clear=True,)        

            return  

######################## SciPy setup ######################################        



    def init_scipy_combo(self):    
        global fit 

        for i in range(len(fit.SciPy_min)):
            self.comboBox_scipy_minimizer_1.addItem('%s'%(fit.SciPy_min[i]),i) 
            self.comboBox_scipy_minimizer_2.addItem('%s'%(fit.SciPy_min[i]),i) 
           
        self.comboBox_scipy_minimizer_1.setCurrentIndex(6)
        self.comboBox_scipy_minimizer_2.setCurrentIndex(0)
            
    def check_scipy_min(self):    
        global fit             
            
        ind_min_1 = self.comboBox_scipy_minimizer_1.currentIndex()
        ind_min_2 = self.comboBox_scipy_minimizer_2.currentIndex()
       

        fit.SciPy_min_use_1 = fit.SciPy_min[ind_min_1]
        fit.SciPy_min_use_2 = fit.SciPy_min[ind_min_2]
        fit.SciPy_min_N_use_1 = int(self.scipy_N_consecutive_iter_1.value())
        fit.SciPy_min_N_use_2 = int(self.scipy_N_consecutive_iter_2.value())
        
        
        fit.Simplex_opt    = {'disp': True, 'maxiter': int(self.simplex_maxiter.value()), 'return_all': False, 'maxfev': int(self.simplex_maxfev.value()), 'xtol':self.simplex_xtol.value() , 'ftol': self.simplex_ftol.value() ,'adaptive':True }
        fit.Powell_opt     = {'disp': True, 'return_all': False, 'maxiter': int(self.powell_maxiter.value()), 'direc': None, 'func': None, 'maxfev': int(self.powell_maxfev.value()), 'xtol': self.powell_xtol.value(), 'ftol': self.powell_ftol.value()}
        fit.CG_opt         = {'disp': True, 'gtol': self.cg_gtol.value(), 'eps': 1.4901161193847656e-08, 'return_all': False, 'maxiter': int(self.cg_maxiter.value()), 'norm': np.inf}
        fit.BFGS_opt       = {'disp': True, 'gtol': self.bfgs_gtol.value(), 'eps': 1.4901161193847656e-08, 'return_all': False, 'maxiter': int(self.bfgs_maxiter.value()), 'norm': np.inf}
        fit.Newton_cg_opt  = {'disp': True, 'xtol': self.Newton_cg_xtol.value(), 'eps': 1.4901161193847656e-08, 'return_all': False, 'maxiter': int(self.Newton_cg_maxiter.value())} 
        fit.L_BFGS_B_opt   = {'disp': True, 'maxcor': int(self.LBFGSB_maxcor.value()), 'ftol': 2.220446049250313e-09, 'gtol': self.LBFGSB_gtol.value(), 'eps': 1e-08, 'maxfun': int(self.LBFGSB_maxiter.value()), 'maxiter': int(self.LBFGSB_maxiter.value()), 'iprint': -1, 'maxls': 20}    
        fit.TNC_opt        = {'disp': True, 'eps': self.TNC_eps.value(), 'scale': None, 'offset': None, 'mesg_num': None, 'maxCGit': int(self.TNC_maxcgit.value()), 'maxiter': int(self.TNC_maxiter.value()), 'eta': self.TNC_eta.value(), 'stepmx':self.TNC_stepmx.value(), 'accuracy': self.TNC_accuracy.value(), 'minfev': self.TNC_minfev.value(), 'ftol': self.TNC_ftol.value(), 'xtol':self.TNC_ftol.value(), 'gtol': self.TNC_gtol.value(), 'rescale': -1 }  
       # fit.COBYLA_opt     = {'disp': True, 'rhobeg': self.cobyla_rhobeg.value(), 'maxiter':  int(self.cobyla_maxiter.value()), 'catol': self.cobyla_catol.value() }
        fit.SLSQP_opt      = {'disp': True, 'maxiter': int(self.slsqp_maxiter.value()),  'eps': 1.4901161193847656e-08, 'ftol': self.slsqp_ftol.value(), 'iprint': 1}
      
        
 

######################## RV plots ######################################        

    def init_gls_norm_combo(self):    
        global fit
        
        self.norms = ['ZK',  'HorneBaliunas', 'Cumming', 'wrms', 'chisq', 'lnL', 'dlnL']
        #'Scargle',
        for i in range(len(self.norms)):
            self.gls_norm_combo.addItem('%s'%(self.norms[i]),i+1)   
            
         
    def run_gls(self):
        global fit
                
        omega = 1/ np.logspace(np.log10(self.gls_min_period.value()), np.log10(self.gls_max_period.value()), num=int(self.gls_n_omega.value()))
        ind_norm = self.gls_norm_combo.currentIndex()

        if len(fit.fit_results.rv_model.jd) > 5:      
            RV_per = gls.Gls((fit.fit_results.rv_model.jd, fit.fit_results.rv_model.rvs, fit.fit_results.rv_model.rv_err), 
            fast=True,  verbose=False, norm=self.norms[ind_norm],ofac=self.gls_ofac.value(), fbeg=omega[-1], fend=omega[0],)
            
            fit.gls = RV_per
        else:
            return
        
        
    def run_gls_o_c(self):
        global fit
                        
        omega = 1/ np.logspace(np.log10(self.gls_min_period.value()), np.log10(self.gls_max_period.value()), num=int(self.gls_n_omega.value()))
        ind_norm = self.gls_norm_combo.currentIndex()
 
        if len(fit.fit_results.rv_model.jd) > 5:
            RV_per_res = gls.Gls((fit.fit_results.rv_model.jd, fit.fit_results.rv_model.o_c, fit.fit_results.rv_model.rv_err), 
            fast=True,  verbose=False, norm= self.norms[ind_norm],ofac=self.gls_ofac.value(), fbeg=omega[-1], fend=omega[ 0],)            
    
            fit.gls_o_c = RV_per_res        
        else:
            return
        

    def update_RV_GLS_plots(self):
        global fit, p7 
 
        p7.plot(clear=True,)   
        

        self.run_gls()
                          
        power_levels = np.array([self.gls_fap1.value(),self.gls_fap2.value(),self.gls_fap3.value()])
  
        if len(fit.fit_results.rv_model.jd) > 5:


            ######################## GLS ##############################
            if self.radioButton_RV_GLS_period.isChecked():
                p7.setLogMode(True,False)        
                p7.plot(1/fit.gls.freq, fit.gls.power,pen='r',symbol=None ) 
                p7.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})    
                
            else:
                p7.setLogMode(False,False)        
                p7.plot(fit.gls.freq, fit.gls.power,pen='r',symbol=None )                    
                p7.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'}) 
                
                
            if fit.gls.norm == 'ZK':
                [p7.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(fit.gls.powerLevel(np.array(power_levels)))]
 
 
            self.RV_periodogram_print_info.clicked.connect(lambda: self.print_info_for_object(
            fit.gls.info(stdout=False) + 
            self.identify_power_peaks(1/fit.gls.freq, fit.gls.power, power_level = power_levels, sig_level = fit.gls.powerLevel(np.array(power_levels)) )))   
    
 
    def update_RV_o_c_GLS_plots(self):
        global fit,  p8  
 
        p8.plot(clear=True,)  
 
        self.run_gls_o_c()
        
        power_levels = np.array([self.gls_fap1.value(),self.gls_fap2.value(),self.gls_fap3.value()])

        if len(fit.fit_results.rv_model.jd) > 5:
 

            ######################## GLS o-c ##############################
            if self.radioButton_RV_o_c_GLS_period.isChecked():
                p8.setLogMode(True,False)        
                p8.plot(1/fit.gls_o_c.freq, fit.gls_o_c.power,pen='r',symbol=None ) 
                p8.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})
 
            else:
                p8.setLogMode(False,False)        
                p8.plot(fit.gls_o_c.freq, fit.gls_o_c.power,pen='r',symbol=None )    
                p8.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'})                
                
            if fit.gls_o_c.norm == 'ZK':
                [p8.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(fit.gls_o_c.powerLevel(np.array(power_levels)))]            

            self.RV_res_periodogram_print_info.clicked.connect(lambda: self.print_info_for_object(fit.gls_o_c.info(stdout=False)+
            self.identify_power_peaks(1/fit.gls_o_c.freq, fit.gls_o_c.power, power_level = power_levels, sig_level = fit.gls_o_c.powerLevel(np.array(power_levels)) ) )  )      
 
 
    
    def update_WF_plots(self):
        global fit, p12  
 
        p12.plot(clear=True,) 
        p12.setLogMode(True,False)
                        
        omega = 1/ np.logspace(np.log10(self.gls_min_period.value()), np.log10(self.gls_max_period.value()),  num=int(self.gls_n_omega.value()))
        #power_levels = np.array([0.1,0.01,0.001])
        
        if len(fit.fit_results.rv_model.jd) > 5:
            ######################## DFT (Window) ##############################
            WF_power = []
            for omi in 2*np.pi*omega: 
                phase = (fit.fit_results.rv_model.jd-fit.fit_results.rv_model.jd[0]) * omi                 
                WC = np.sum(np.cos(phase))
                WS = np.sum(np.sin(phase))
                WF_power.append((WC**2 + WS**2)/len(fit.fit_results.rv_model.jd)**2) 

            WF_power = np.array(WF_power)
            ######################## GLS o-c ##############################
            if self.radioButton_RV_WF_period.isChecked():
                p12.setLogMode(True,False)        
                p12.plot(1/np.array(omega), WF_power,pen='k',symbol=None )   
                p12.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})
            else:
                p12.setLogMode(False,False)        
                p12.plot(np.array(omega), WF_power,pen='k',symbol=None )   
                p12.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'})      


                        
            self.WF_print_info.clicked.connect(lambda: self.print_info_for_object(self.identify_power_peaks(1/np.array(omega), WF_power)))        
         
            #self.lineEdit

    def rv_GP_set_use(self):

        if self.do_RV_GP.isChecked():
            fit.doGP = True
        else:
            fit.doGP = False
            

    def update_RV_plots(self):
        global fit, p1,p2
 
        p1.plot(clear=True,)
        p2.plot(clear=True,)
 
    
        self.check_RV_symbol_sizes()
        
        #inf1 = pg.InfiniteLine(movable=False, angle=0, label=None, span=(0, 1), 
        #              labelOpts={'position':0.0, 'color': 'k', 'fill': (200,200,200,50), 'movable': False} )
        #p1.addItem(inf1)    

        if len(fit.filelist.idset)==0:
            return

        if self.jitter_to_plots.isChecked():
            error_list = self.add_jitter(fit.fit_results.rv_model.rv_err, fit.filelist.idset)
        else:
            error_list = fit.fit_results.rv_model.rv_err
 
        p1.addLine(x=None, y=0, pen=pg.mkPen('#ff9933', width=0.8))
 
 
        if fit.doGP == True:
            y_model = fit.fit_results.model + fit.gp_model_curve[0]
            y_model_o_c = fit.gp_model_curve[0]
        else:
            y_model = fit.fit_results.model 
            y_model_o_c = np.zeros(len(y_model))

        p1.plot(fit.fit_results.model_jd,y_model, 
        pen={'color': 0.5, 'width': 1.1},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
        viewRect=True, labels =  {'left':'RV', 'bottom':'JD'}) 
        
        if  fit.doGP == True:
            pfill = pg.FillBetweenItem(p1.plot(fit.fit_results.model_jd, fit.fit_results.model + fit.gp_model_curve[0]+fit.gp_model_curve[2]), 
                                       p1.plot(fit.fit_results.model_jd, fit.fit_results.model + fit.gp_model_curve[0]-fit.gp_model_curve[2]), 
                                       brush = pg.mkColor(244,140,66,128))
            p1.addItem(pfill)  
            
            
        for i in range(max(fit.filelist.idset)+1):
            p1.plot(fit.fit_results.rv_model.jd[fit.filelist.idset==i],fit.fit_results.rv_model.rvs[fit.filelist.idset==i], 
            pen=None, #{'color': colors[i], 'width': 1.1},
            symbol=fit.pyqt_symbols_rvs[i],
            symbolPen={'color': fit.colors[i], 'width': 1.1},
            symbolSize=fit.pyqt_symbols_size_rvs[i],enableAutoRange=True,viewRect=True,
            symbolBrush=fit.colors[i]
            )        
            err1 = pg.ErrorBarItem(x=fit.fit_results.rv_model.jd[fit.filelist.idset==i], 
                                   y=fit.fit_results.rv_model.rvs[fit.filelist.idset==i],symbol='o', 
            height=error_list[fit.filelist.idset==i], beam=0.0, pen=fit.colors[i])  

            p1.addItem(err1)  
 
        p2.addLine(x=None, y=0, pen=pg.mkPen('#ff9933', width=0.8))

        p2.plot(fit.fit_results.model_jd,y_model_o_c, 
        pen={'color': 0.5, 'width': 1.1},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
        viewRect=True, labels =  {'left':'RV', 'bottom':'JD'}) 
        
        if fit.doGP == True:
            pfill_o_c = pg.FillBetweenItem(p2.plot(fit.fit_results.model_jd, fit.gp_model_curve[0]+fit.gp_model_curve[2]), 
                                           p2.plot(fit.fit_results.model_jd, fit.gp_model_curve[0]-fit.gp_model_curve[2]), 
                                           brush = pg.mkColor(244,140,66,128))
            p2.addItem(pfill_o_c)  
        
        
        for i in range(max(fit.filelist.idset)+1):
            p2.plot(fit.fit_results.rv_model.jd[fit.filelist.idset==i],fit.fit_results.rv_model.o_c[fit.filelist.idset==i], 
            pen=None, #{'color': colors[i], 'width': 1.1},
            symbol=fit.pyqt_symbols_rvs[i],
            symbolPen={'color': fit.colors[i], 'width': 1.1},
            symbolSize=fit.pyqt_symbols_size_rvs[i],enableAutoRange=True,viewRect=True,
            symbolBrush=fit.colors[i]
            )        
            err2 = pg.ErrorBarItem(x=fit.fit_results.rv_model.jd[fit.filelist.idset==i], 
                                   y=fit.fit_results.rv_model.o_c[fit.filelist.idset==i],symbol='o', 
            height=error_list[fit.filelist.idset==i], beam=0.0, pen=fit.colors[i])  

            p2.addItem(err2)  
 
     
        
    def update_plots(self):
        self.update_RV_GLS_plots()
        self.update_RV_o_c_GLS_plots()    
        self.update_WF_plots()                
        self.update_RV_plots()
        self.update_extra_plots()
        self.update_orb_plot()
        #self.change_extra_plot()
        self.update_transit_plots()    
        

################################ RV files #######################################################
        
    def showDialog_fortran_input_file(self):
        global fit, ses_list
 
        input_files = QtGui.QFileDialog.getOpenFileName(self, 'Open session', '', 'Data (*.init)')
        
        if str(input_files[0]) != '':
            fit_new=rv.signal_fit(str(input_files[0]), 'Test',readinputfile=True)
            
            if len(ses_list) == 1:
                ses_list[0] = fit_new
                fit = fit_new
            else:
                ses_list.append(fit_new)
                
            self.session_list()
            self.update_use_from_input_file()
            self.init_fit()
            self.update_RV_file_buttons()

    def showDialog_RV_input_file(self):
        global fit

        but_ind = self.buttonGroup_4.checkedId()   
        input_files = QtGui.QFileDialog.getOpenFileName(self, 'Open RV data', '', 'Data (*.vels)')
        
        if str(input_files[0]) != '':
 
            fit.add_dataset(self.file_from_path(input_files[0]), str(input_files[0]),0.0,1.0)
            #### new stuf ####
            fit.add_rv_dataset('test', str(input_files[0]),rv_idset =but_ind-1)
            ##################
            self.init_fit()            
            self.update_use_from_input_file()            
            self.update_use()
            self.update_params()
            self.update_RV_file_buttons()
            #self.buttonGroup_4.button(fit.filelist.ndset).setText(self.file_from_path(input_files[0]))
            

   # def RV_file_names(self,ind,name):
   #     global fit
   #     rv_file_namez = ["data 1","data 2","data 3","data 4","data 5","data 6","data 7","data 8","data 9","data 10"]

    def remove_RV_file(self):
        global fit

        but_ind = self.buttonGroup_remove_RV_data.checkedId()   
        fit.remove_dataset(but_ind -1)
        #### new stuf ####
        fit.remove_rv_dataset(but_ind -1)
        #### new stuf ####
       
        self.init_fit()         
        self.update_use_from_input_file()   
        self.update_use()
        self.update_gui_params()
        self.update_params()
        self.update_RV_file_buttons()

    def update_RV_file_buttons(self):
        global fit, colors    
        
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        #font.setWeight(75)
        
        for i in range(10):
            if i < fit.filelist.ndset:
                self.buttonGroup_4.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
                self.buttonGroup_remove_RV_data.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
                self.buttonGroup_4.button(i+1).setText(fit.filelist.files[i].name) 
                self.buttonGroup_4.button(i+1).setFont(font)

            else:
                self.buttonGroup_4.button(i+1).setStyleSheet("")
                self.buttonGroup_remove_RV_data.button(i+1).setStyleSheet("")
                self.buttonGroup_4.button(i+1).setText("data %s"%(i+1))

                #"background-color: #333399;""background-color: yellow;" "selection-color: yellow;"  "selection-background-color: blue;")               
        self.init_correlations_combo()


################################ transit files #######################################################      

    def showDialog_tra_input_file(self):
        global fit

        but_ind = self.buttonGroup_transit_data.checkedId()   
        input_files = QtGui.QFileDialog.getOpenFileName(self, 'Open Transit data', '', 'Data (*.tran)')

        if str(input_files[0]) != '':
 
            fit.add_transit_dataset('test', str(input_files[0]),tra_idset =but_ind-1)
            self.update_use_from_input_file()            
            self.update_use()
            self.update_gui_params()
             
            self.update_params()
            self.update_tra_file_buttons()
            self.buttonGroup_transit_data.button(but_ind).setText(self.file_from_path(input_files[0]))
            
            self.tab_timeseries_RV.setCurrentWidget(self.Phot_timeseries_plot)

            
    def remove_tra_file(self):
        global fit

        but_ind = self.buttonGroup_remove_transit_data.checkedId()   
        fit.remove_transit_dataset(but_ind -1)
       # self.init_fit()         
      #  self.update_use_from_input_file()   
      #  self.update_use()
      #  self.update_gui_params()
     #   self.update_params()
        self.update_tra_file_buttons()


    def update_tra_file_buttons(self):
        global fit, colors          

        for i in range(10):
            if len(fit.tra_data_sets[i]) != 0:
                self.buttonGroup_transit_data.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
                self.buttonGroup_remove_transit_data.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
            else:
                self.buttonGroup_transit_data.button(i+1).setStyleSheet("")
                self.buttonGroup_remove_transit_data.button(i+1).setStyleSheet("")
                self.buttonGroup_transit_data.button(i+1).setText("data %s"%(i+1))

                #"background-color: #333399;""background-color: yellow;" "selection-color: yellow;"  "selection-background-color: blue;")               
        self.update_transit_plots()
 

################################ activity files #######################################################
        
    def showDialog_act_input_file(self):
        global fit

        but_ind = self.buttonGroup_activity_data.checkedId()   
        input_files = QtGui.QFileDialog.getOpenFileName(self, 'Open Activity data', '', 'Data (*.act)')

        if str(input_files[0]) != '':
 
            fit.add_act_dataset('test', str(input_files[0]),act_idset =but_ind-1)
            #self.init_fit()            
            #self.update_use_from_input_file()            
            #self.update_use()
            #self.update_params()
            self.update_act_file_buttons()
            self.update_activity_gls_plots(but_ind-1)
            self.buttonGroup_activity_data.button(but_ind).setText(self.file_from_path(input_files[0]))

            #self.handleActivated_act_gls(but_ind-1)
            
    def remove_act_file(self):
        global fit

        but_ind = self.buttonGroup_remove_activity_data.checkedId()   
        fit.remove_act_dataset(but_ind -1)
       # self.init_fit()         
      #  self.update_use_from_input_file()   
      #  self.update_use()
      #  self.update_gui_params()
     #   self.update_params()
        self.update_act_file_buttons()

    def update_act_file_buttons(self):
        global fit, colors          

        for i in range(10):
            if len(fit.act_data_sets[i]) != 0:
                self.buttonGroup_activity_data.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
                self.buttonGroup_remove_activity_data.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
            else:
                self.buttonGroup_activity_data.button(i+1).setStyleSheet("")
                self.buttonGroup_remove_activity_data.button(i+1).setStyleSheet("")
                self.buttonGroup_activity_data.button(i+1).setText("data %s"%(i+1))

                #"background-color: #333399;""background-color: yellow;" "selection-color: yellow;"  "selection-background-color: blue;")               
        self.init_correlations_combo()


##################################### Various ################################# 


    def init_fit(self): 
        global fit
        minimize_fortran=True
        if fit.model_saved == False or len(fit.fit_results.rv_model.jd) != len(fit.filelist.idset):
            fit.fitting(fileinput=False,outputfiles=[1,1,1], minimize_fortran=minimize_fortran,  fortran_kill=self.dyn_model_to_kill.value(), timeout_sec=self.master_timeout.value(), minimize_loglik=True,amoeba_starts=0, print_stat=False, eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value(), npoints=self.points_to_draw_model.value(), model_max= self.model_max_range.value(), model_min= self.model_min_range.value())
            #self.worker_RV_fitting(, ff=0, m_ln=True, auto_fit = False , init = True ):
            #self.fit_dispatcher(init=False)
            for i in range(fit.npl):
                 rv.phase_RV_planet_signal(fit,i+1)       
                 
        self.update_labels()
        self.update_gui_params()
        self.update_errors() 
        self.update_a_mass() 
        
        #start_time = time.time()
        self.update_plots() 
        self.update_transit_plots() 
        #print("--- %s seconds ---" % (time.time() - start_time))      
        self.jupiter_push_vars()       
        
        
    def update_orb_plot(self):
        global fit, p15
        
        p15.plot(clear=True,)    
        
        for i in range(fit.npl):
            orb_xyz, pl_xyz, peri_xyz, apo_xyz = rv.planet_orbit_xyz(fit,i)        
            p15.plot(orb_xyz[0],orb_xyz[1], pen={'color': 0.5, 'width': 1.1},enableAutoRange=True,viewRect=True)   
            p15.plot((0,peri_xyz[0]),(0,peri_xyz[1]), pen={'color': 0.5, 'width': 1.1},enableAutoRange=True,viewRect=True)               
            
            p15.plot((pl_xyz[0],pl_xyz[0]), (pl_xyz[1],pl_xyz[1] ), pen=None,symbol='o', symbolSize=6,enableAutoRange=True,viewRect=True, symbolBrush='b') 
            
        p15.plot(np.array([0,0]), np.array([0,0]), pen=None,symbol='o', symbolSize=8,enableAutoRange=True,viewRect=True, symbolBrush='r')                



            
            
  
    def add_jitter(self, errors, ind):
        global fit
        
        errors_with_jitt = np.array([np.sqrt(errors[i]**2 + fit.params.jitters[ii]**2)  for i,ii in enumerate(ind)])
        
        return errors_with_jitt


################ EXTRA PLOTS (work in progress) ######################
        
    
    
    def update_extra_plots(self):
        global fit

        self.comboBox_extra_plot.clear()
        self.comboBox_extra_plot.setObjectName("which plot")       
        
        #self.check_RV_symbol_sizes()


        if fit.npl != 0:
            for i in range(fit.npl):
                self.comboBox_extra_plot.addItem('phase pl %s'%(i+1),i+1)
            
            self.comboBox_extra_plot.addItem('RV GLS',fit.npl+1)
            self.comboBox_extra_plot.addItem('RV GLS o-c',fit.npl+2)

            self.phase_plots(1)   
            
        self.comboBox_extra_plot.activated.connect(self.handleActivated)        

     


 
    def handleActivated(self, index):
        global fit, pe, p2
        
        ind = self.comboBox_extra_plot.itemData(index) 
 
        if ind <= fit.npl:
            self.phase_plots(ind)
        elif ind == fit.npl+1: 
            self.extra_RV_GLS_plots()
        elif ind == fit.npl+2: 
            self.extra_RV_GLS_o_c_plots()            
            #pe.setYLink(p2)
           # pe.setXLink(p2)

            #gg = p2.getPlotItem().getViewBox()
         #   hh = gg.getViewBox()
         #   pe.scene().addItem(gg)   
         #   pe.scene().addItem(gg)
        else:
            return

    def phase_plots(self, ind, offset = 0):
        global fit, colors   
        
        pe.plot(clear=True,)    
        pe.setLogMode(False,False)        

    
        ph_data = fit.ph_data[ind-1]
        ph_model = fit.ph_model[ind-1] #rv.phase_RV_planet_signal(fit,ind)


        offset = (self.RV_phase_slider.value()/100.0)* fit.params.planet_params[7*(ind-1)+1] 

        if len(ph_data) == 1:
            return

        if self.jitter_to_plots.isChecked():
            error_list = self.add_jitter(ph_data[2], ph_data[3])
        else:
            if len(ph_data) != 0:
                error_list = ph_data[2]
            else:
                return



        model_time_phase = np.array((ph_model[0]-offset)%fit.params.planet_params[7*(ind-1)+1] )
                             
        sort = sorted(range(len(model_time_phase)), key=lambda k: model_time_phase[k])                        
        model_time_phase  = model_time_phase[sort] 
        ph_model =  ph_model[1][sort] 
        #print(model_time_phase[0:10],sort[0:10])
 
        pe.addLine(x=None, y=0, pen=pg.mkPen('#ff9933', width=0.8))   
        pe.plot(model_time_phase,ph_model, pen={'color': 0.5, 'width': 2.0},
        enableAutoRange=True,viewRect=True, labels =  {'left':'RV', 'bottom':'JD'})   
        
        
        
        
        for i in range(max(ph_data[3])+1):
        
            pe.plot((ph_data[0][ph_data[3]==i]-offset)%fit.params.planet_params[7*(ind-1)+1],ph_data[1][ph_data[3]==i],             
            pen=None, #{'color': colors[i], 'width': 1.1},
            symbol=fit.pyqt_symbols_rvs[i],
            symbolPen={'color': fit.colors[i], 'width': 1.1},
            symbolSize=fit.pyqt_symbols_size_rvs[i],enableAutoRange=True,viewRect=True,
            symbolBrush=fit.colors[i]
            )  
               
            err_ = pg.ErrorBarItem(x=(ph_data[0][ph_data[3]==i]-offset)%fit.params.planet_params[7*(ind-1)+1], y=ph_data[1][ph_data[3]==i],
            symbol=fit.pyqt_symbols_rvs[i], height=error_list[ph_data[3]==i], beam=0.0, pen=fit.colors[i])   
         
            pe.addItem(err_)
        
        pe.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})
        pe.setLabel('left',   'RV', units='m/s',  **{'font-size':'12pt'})  

    ############### VERY VERY VERY Ugly fix !!!! it should be 
    
    def extra_RV_GLS_plots(self):
        global fit,  pe 
 
        pe.plot(clear=True,)   
        power_levels = np.array([self.gls_fap1.value(),self.gls_fap2.value(),self.gls_fap3.value()])

 
        ######################## GLS ##############################
        if self.radioButton_RV_GLS_period.isChecked():
            pe.setLogMode(True,False)        
            pe.plot(1/fit.gls.freq, fit.gls.power, pen='r',symbol=None ) 
            pe.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})    
            pe.setLabel('left', 'Power', units='',  **{'font-size':'12pt'})    
           
        else:
            pe.setLogMode(False,False)        
            pe.plot(fit.gls.freq, fit.gls.power, pen='r',symbol=None )                    
            pe.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'}) 
            pe.setLabel('left', 'Power', units='',  **{'font-size':'12pt'})    

        if fit.gls.norm == 'ZK':
            [pe.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(fit.gls.powerLevel(np.array(power_levels)))]

    def extra_RV_GLS_o_c_plots(self):
        global fit,  pe 
 
        pe.plot(clear=True,)           
        power_levels = np.array([self.gls_fap1.value(),self.gls_fap2.value(),self.gls_fap3.value()])
        
        
        ######################## GLS o-c ##############################
        if self.radioButton_RV_o_c_GLS_period.isChecked():
            pe.setLogMode(True,False)        
            pe.plot(1/fit.gls_o_c.freq, fit.gls_o_c.power, pen='r',symbol=None ) 
            pe.setLabel('bottom', 'days', units='',  **{'font-size':'12pt'})    
            pe.setLabel('left', 'Power', units='',  **{'font-size':'12pt'})    
           
        else:
            pe.setLogMode(False,False)        
            pe.plot(fit.gls_o_c.freq, fit.gls_o_c.power, pen='r',symbol=None )                    
            pe.setLabel('bottom', 'frequency', units='',  **{'font-size':'12pt'}) 
            pe.setLabel('left', 'Power', units='',  **{'font-size':'12pt'})    


        if fit.gls.norm == 'ZK':
            [pe.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(fit.gls_o_c.powerLevel(np.array(power_levels)))]



############ TLS (Work in progress here) ##############################      
       
    def worker_tls_complete(self):
        global fit  
 
              
        self.update_tls_plots()                   
        self.statusBar().showMessage('')   
 
        self.jupiter_push_vars()   
        self.calc_TLS.setEnabled(True)         
 
    def worker_tls(self):
        global fit  
        
        #if sys.version_info[0] == 2:
        ##    print("TLS not working with Py2 at the moment") 
        #    return
        if tls_not_found==True:
            print("TLS Not found, try to install with 'pip install transitleastsquares'") 
            return

        
        #print("test")
        self.calc_TLS.setEnabled(False)         
 
        
        # check if transit data is present
        z=0
        for i in range(10):
            if len(fit.tra_data_sets[i]) != 0:
                z=z+1
        
        if z <= 0:
            choice = QtGui.QMessageBox.information(self, 'Warning!',
            "Not possible to look for planets if there are no transit data loaded. Please add your transit data first. Okay?", QtGui.QMessageBox.Ok)      
            self.calc_TLS.setEnabled(True)         
            return   

        self.statusBar().showMessage('Looking for Transit events (TLS).... ')                 
        worker_tls = Worker(self.tls_search)# Any other args, kwargs are passed to the run  
 
        worker_tls.signals.finished.connect(self.worker_tls_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker_tls)       
     

    def tls_search(self):
        global fit
        
        tls_model = transitleastsquares(fit.tra_data_sets[0][0], fit.tra_data_sets[0][1])
        tls_results = tls_model.power(oversampling_factor=int(self.tls_ofac.value()), duration_grid_step=self.tls_grid_step.value())
    
        fit.tls = tls_results  # TB Fixed with an rvmod object (i.e. fit.tls_obj)
        
        
        #print("testeeee",self.tls_obj)
        
    def update_tls_plots(self): 
        global fit, p9, colors
    
        p9.plot(clear=True,) 
            
        if len(fit.tra_data_sets[0]) != 0:
            #t = fit.tra_data_sets[0][0]
            #flux = fit.tra_data_sets[0][1]
           # flux_err = fit.tra_data_sets[0][2]
           
            text = '''
Period: %s d   
Transit depth: %s 
Transit duration: %s d
'''%(fit.tls.period,fit.tls.depth,fit.tls.duration)
           
            p9.plot(fit.tls.periods, fit.tls.power,        
            pen='r',  enableAutoRange=True,viewRect=True)
#0.9      5.7
#0.95     6.1
#0.99     7.0
#0.999    8.3
#0.9999   9.1
            [p9.addLine(x=None, y=fap, pen=pg.mkPen('k', width=0.8, style=QtCore.Qt.DotLine)) for ii,fap in enumerate(np.array([5.7,7.0,8.3]))]
   
 
            self.tls_print_info.clicked.connect(lambda: self.print_info_for_object(text))            
            return

        else:    
            text_err = pg.TextItem('Nothing to plot',color=(0,0,0))#, anchor=(0,0), border='w',color) #, fill=(0, 0, 255, 100))
            p9.addItem(text_err, ignoreBounds=True)   
            self.tls_print_info.clicked.connect(lambda: self.print_info_for_object(""))            
            return


        
 ############ transit fitting (Work in progress here) ##############################      
       
    def worker_transit_fitting_complete(self):
        global fit  
        
        self.update_labels()
        self.update_gui_params()
        self.update_errors() 
        self.update_a_mass()                 
        self.update_transit_plots()  
                 
        self.statusBar().showMessage('')  
        
        if fit.rtg[0]:
            for i in range(fit.npl):
                rv.phase_RV_planet_signal(fit,i+1)        
            self.update_plots()  
            
            
        self.jupiter_push_vars()   
        self.button_fit.setEnabled(True)         
 
    def worker_transit_fitting(self, ff=1, auto_fit = False ):
        global fit  
        
        self.button_fit.setEnabled(False)         
        self.update_params() 
        self.update_use()   
        
        # check if transit data is present
        z=0
        for i in range(10):
            if len(fit.tra_data_sets[i]) != 0:
                z=z+1
        
        if z <= 0:
            choice = QtGui.QMessageBox.information(self, 'Warning!',
            "Not possible to look for planets if there are no transit data loaded. Please add your transit data first. Okay?", QtGui.QMessageBox.Ok)      
            self.button_fit.setEnabled(True)         
            return 
        
        if fit.rtg[0] == True:
             if fit.filelist.ndset <= 0:
                 choice = QtGui.QMessageBox.information(self, 'Warning!',
                 "Not possible to look for planets if there are no RV data loaded. Please add your RV data first. Okay?", QtGui.QMessageBox.Ok)      
                 self.button_fit.setEnabled(True)         
                 return   

        if fit.rtg[0] == True:        
            self.statusBar().showMessage('Minimizing Transit + RV parameters.... SciPy in action, please be patient.  ')       
        else:
            self.statusBar().showMessage('Minimizing Transit parameters.... SciPy in action, please be patient. ')       
           

        self.check_scipy_min()
        fit.model_npoints = self.points_to_draw_model.value()

          
        worker4 = Worker(lambda:  self.transit_fit(ff=ff ) )# Any other args, kwargs are passed to the run  
 
        worker4.signals.finished.connect(self.worker_transit_fitting_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker4)       
     

    def transit_fit(self, ff=0 ):
        global fit
        
        
        # this is only a simple hack.. junk removed later on
        if ff ==0:
            old_t0_use = fit.t0_use
            old_pl_a_use = fit.pl_a_use
            old_pl_rad_use = fit.pl_rad_use
            old_rv_use = fit.use.use_planet_params
            old_rvoff_use = fit.use.use_offsets
            old_rvjitt_use = fit.use.use_jitters
            old_tra_off_use = fit.tra_off
            old_tra_jitt_use = fit.tra_jitt
            
            
            for i in range(fit.npl):
                fit.t0_use[i] = False
                fit.pl_a_use[i] = False
                fit.pl_rad_use[i] = False 
                fit.use.use_planet_params[i*7] = False 
                fit.use.use_planet_params[i*7+1] = False 
                fit.use.use_planet_params[i*7+2] = False 
                fit.use.use_planet_params[i*7+3] = False 
                fit.use.use_planet_params[i*7+4] = False 
                fit.use.use_planet_params[i*7+5] = False 
                fit.use.use_planet_params[i*7+6] = False 
            for i in range(10): 
                fit.use.use_jitters[i] = False
                fit.use.use_offsets[i] = False   
                fit.tra_off_use[i] = False
                fit.tra_jitt_use[i] = False
            #old_tra_use = fit.tr_params_use 
            #fit.tr_params_use = [False, False,False,False,False,False,False]
            #rv.run_SciPyOp_transit(fit)
            rv.run_SciPyOp(fit)
            
            for i in range(fit.npl):
                fit.t0_use[i] = old_t0_use[i]
                fit.pl_a_use[i] = old_pl_a_use[i]
                fit.pl_rad_use[i] = old_pl_rad_use[i]             
                fit.use.use_planet_params[i*7] = old_rv_use[i*7]  
                fit.use.use_planet_params[i*7+1] = old_rv_use[i*7+1]  
                fit.use.use_planet_params[i*7+2] = old_rv_use[i*7+2] 
                fit.use.use_planet_params[i*7+3] = old_rv_use[i*7+3] 
                fit.use.use_planet_params[i*7+4] = old_rv_use[i*7+4]  
                fit.use.use_planet_params[i*7+5] = old_rv_use[i*7+5]  
                fit.use.use_planet_params[i*7+6] = old_rv_use[i*7+6] 
            for i in range(10): 
                fit.use.use_jitters[i] =  old_rvjitt_use[i]  
                fit.use.use_offsets[i] =  old_rvoff_use[i]  
                fit.tra_off_use[i] = old_tra_off_use[i]
                fit.tra_jitt_use[i] = old_tra_jitt_use[i]                
                
        else:
       # rv.run_SciPyOp_transit(fit)
            rv.run_SciPyOp(fit)
 
    def update_transit_plots(self): 
        global fit, p3, colors
    
        p3.plot(clear=True,) 
        p4.plot(clear=True,)         
           

        tr_files = []
        
        for i in range(10):
            if len(fit.tra_data_sets[i]) != 0:
                tr_files.append(fit.tra_data_sets[i])
        
        for j in range(len(tr_files)):        
        
        #if len(fit.tra_data_sets[0]) != 0:
            t = tr_files[j][0]
            flux = tr_files[j][1] + fit.tra_off[j]
            flux_err = np.sqrt(tr_files[j][2]**2 + fit.tra_jitt[j]**2)
            
            
            
            fit.prepare_for_mcmc(rtg = fit.rtg)    
            par = np.array(fit.parameters)  

            flux_model =[1]*len(flux)
            m =  {k: [] for k in range(9)}
             
            for i in range(fit.npl):
                
                fit.tr_params.per = par[fit.filelist.ndset*2 +7*i+1] #1.0    #orbital period
                fit.tr_params.ecc = par[fit.filelist.ndset*2 +7*i+2] #0.0  
                fit.tr_params.w   = par[fit.filelist.ndset*2 +7*i+3] #90.0   #longitude of periastron (in degrees)               
                fit.tr_params.inc = par[fit.filelist.ndset*2 +7*i+5]#90. #orbital inclination (in degrees)
            
               # par[len(vel_files)*2 +7*npl +5 + 3*i] = t_transit
            
               # if fit.rtg[0] == True:
               #     t_peri, t_transit = rv.transit_tperi(par[fit.filelist.ndset*2 +7*i+1], par[fit.filelist.ndset*2 +7*i+2], 
               #                                           par[fit.filelist.ndset*2 +7*i+3], par[fit.filelist.ndset*2 +7*i+4], fit.epoch)
                   # t00 = par[fit.filelist.ndset*2 +7*i+1] - (fit.epoch%par[fit.filelist.ndset*2 +7*i+1]) + (t_transit-fit.epoch)
               #     t00 = par[fit.filelist.ndset*2 +7*i+1] -  t_transit 
                   
               #     fit.tr_params.t0  = par[fit.filelist.ndset*2 +7*fit.npl +5 + 3*i] = t00%par[fit.filelist.ndset*2 +7*i+1]  #= (t_transit-epoch)%par[len(vel_files)*2 +7*i+1]#0.0  #time of inferior conjunction
               # else:
               #     fit.tr_params.t0  = par[fit.filelist.ndset*2 +7*fit.npl +5 + 3*i]   #= (t_transit-epoch)%par[len(vel_files)*2 +7*i+1]#0.0  #time of inferior conjunction
               #     
                    
                fit.tr_params.t0  = par[fit.filelist.ndset*2  +7*fit.npl +5 + 3*i]                
                fit.tr_params.a   = par[fit.filelist.ndset*2  +7*fit.npl +5 + 3*i+1] #15  #semi-major axis (in units of stellar radii)
                fit.tr_params.rp  = par[fit.filelist.ndset*2  +7*fit.npl +5 + 3*i+2] #0.15   #planet radius (in units of stellar radii)
                #print(tr_params.t0)
                #print(tr_params.per, tr_params.ecc,tr_params.w, tr_params.inc, tr_params.t0,tr_params.a,tr_params.rp )
        
                m[i] = batman.TransitModel(fit.tr_params, t)    #initializes model
     
                flux_model = flux_model * m[i].light_curve(fit.tr_params)       
                #calculates light curve  
            tr_o_c = flux -flux_model
 
         
            
            p3.plot(t, flux,        
            pen=None,  
            symbol='o',
            symbolPen={'color': fit.tra_colors[j], 'width': 1.1},
            symbolSize=self.transit_data_size.value(),enableAutoRange=True,viewRect=True,
            symbolBrush=fit.tra_colors[j] ) 
            
            err_ = pg.ErrorBarItem(x=t, y=flux,
            symbol='o', height=flux_err, beam=0.0, pen=fit.tra_colors[j])   
     
            p3.addItem(err_)            
            
           # m = batman.TransitModel(fit.tr_params, t)    #initializes model
 
            #flux_model = m.light_curve(fit.tr_params)          #calculates light curve           
            p3.plot(t, flux_model,pen='k',symbol=None )    
            
            p4.plot(t, tr_o_c,        
            pen=None,  
            symbol='o',
            symbolPen={'color': fit.tra_colors[j], 'width': 1.1},
            symbolSize=self.transit_data_size.value(),enableAutoRange=True,viewRect=True,
            symbolBrush=fit.tra_colors[j] )             

            err_ = pg.ErrorBarItem(x=t, y=flux-flux_model,
            symbol='o', height=flux_err, beam=0.0, pen=fit.tra_colors[j])               
            p4.addItem(err_)   
                     
        #else:    
        #    t = np.linspace(-0.25, 0.25, 1000)  #times at which to calculate light curve   
        #    m = batman.TransitModel(fit.tr_params, t)    #initializes model
        #    flux_model = m.light_curve(fit.tr_params)          #calculates light curve
 
        #    p3.plot(t, flux_model,pen='k',symbol=None )     
  

 
        
############################# N-Body ########################################        

    def worker_Nbody_complete(self):
        global fit, colors, p13, p14  

        p13.plot(clear=True,)
        p14.plot(clear=True,)

        for i in range(fit.npl):
            p13.plot(fit.evol_T[i], fit.evol_a[i] ,pen=fit.colors[i],symbol=None )     
            p14.plot(fit.evol_T[i], fit.evol_e[i] ,pen=fit.colors[i],symbol=None )   
             
        self.button_orb_evol.setEnabled(True)       
        self.statusBar().showMessage('')           
          
 
    def worker_Nbody(self):
        global fit  

        self.button_orb_evol.setEnabled(False)         
        
        # check if any fits where performed, and tus planets present
        if fit.fit_results.mass <= 0:
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "Not possible to integrate a fit that does not exist. First perform an orbital fitting and then test the orbital stability. Okay?", QtGui.QMessageBox.Ok)      
             self.button_orb_evol.setEnabled(True)         
             return        

        if fit.npl < 2:
            choice = QtGui.QMessageBox.information(self, 'Warning!'," With less than two planets this makes no sense. Okay?",
                                            QtGui.QMessageBox.Ok) 
            return
 
        self.statusBar().showMessage('Running Orbital Evolution......')   
        
        # Pass the function to execute
        worker3 = Worker(lambda: self.run_orbital_simulations()) # Any other args, kwargs are passed to the run  
        # Execute
        worker3.signals.finished.connect(self.worker_Nbody_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker3)  

 
    def run_orbital_simulations(self):
        global fit

        self.max_time_of_evol

        if self.radioButton_SyMBA.isChecked():
            integrator = 'symba'
        elif self.radioButton_MVS.isChecked():
            integrator = 'mvs'        
        elif self.radioButton_MVS_GR.isChecked():       
             integrator = 'mvs_gr'       
        
        fit.run_stability_last_fit_params(timemax=self.max_time_of_evol.value(), timestep=self.time_step_of_evol.value(), integrator=integrator)      
        
                
       
############################# Fortran fitting ###############################        
        
    def worker_RV_fitting_complete(self):
        global fit  
        
        self.update_labels()
        self.update_gui_params()
        self.update_errors() 
        self.update_a_mass()                    
                 
        self.statusBar().showMessage('')   
        #self.console_widget.print_text(str(fit.print_info(short_errors=False))) 

        self.jupiter_push_vars()   
        self.button_fit.setEnabled(True)       
        self.update_plots()  
 
    def worker_RV_fitting(self, ff=20, m_ln=True, auto_fit = False , init = False ):
        global fit  
        
        self.button_fit.setEnabled(False)         
        
        # check if RV data is present
        if fit.filelist.ndset <= 0:
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "Not possible to look for planets if there are no RV data loaded. Please add your RV data first. Okay?", QtGui.QMessageBox.Ok)      
             self.button_fit.setEnabled(True)         
             return   
         
            
        self.check_bounds()
        self.check_priors()   
        
        fit.model_npoints = self.points_to_draw_model.value()
        #self.tabWidget_helper.setCurrentWidget(self.tab_info)
        
        
        if self.radioButton_fortran77.isChecked() and not self.do_RV_GP.isChecked() or init == True:
            self.statusBar().showMessage('Minimizing parameters....')    
            if init == True:
                ff = 0
                doGP=False
            else:
                doGP=self.do_RV_GP.isChecked()
            # Pass the function to execute
            worker2 = Worker(lambda:  self.optimize_fit(ff=ff, doGP=doGP, minimize_fortran=True, m_ln=m_ln, auto_fit = auto_fit)) # Any other args, kwargs are passed to the run  
 
        else:         
            self.check_scipy_min()

            self.statusBar().showMessage('Minimizing parameters using SciPyOp (might be slow)....')                 
            worker2 = Worker(lambda:  self.optimize_fit(ff=0, doGP=self.do_RV_GP.isChecked(),  gp_kernel_id=-1, minimize_fortran=False, m_ln=m_ln, auto_fit = auto_fit)) # Any other args, kwargs are passed to the run  
            self.tabWidget_helper.setCurrentWidget(self.tab_info)
            
            
        worker2.signals.finished.connect(self.worker_RV_fitting_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker2) 
        

     
    def update_dyn_kep_flag(self):

        if self.radioButton_Dynamical.isChecked():
            fit.mod_dynamical = True
        else:
            fit.mod_dynamical = False
            
            
            
    def optimize_fit(self,ff=20,m_ln=True, doGP=False, gp_kernel_id=-1, auto_fit = False, minimize_fortran=True):  
        global fit
        
        if not auto_fit:
            self.update_params()
 
            
        if self.radioButton_Dynamical.isChecked():
            #fit.mod_dynamical = True
            f_kill = self.dyn_model_to_kill.value()
            if ff > 1:
                ff = 1 #TBF
           # ff = 1
        else:
            #fit.mod_dynamical = False
            f_kill = self.kep_model_to_kill.value()    
        
        if minimize_fortran==False:
            ff = 0 
            
      #  print(ff)   

        if m_ln == True and doGP == False:
           # if ff > 0:        
           #     """
           #     run one time using the L-M method ignorring the jitter (for speed)
          #      """
               # fit.fitting(fileinput=False,outputfiles=[1,0,0], doGP=doGP, kernel_id=gp_kernel_id, minimize_fortran=minimize_fortran, fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=False,amoeba_starts=ff, print_stat=False, eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value())
            """
            now run the amoeba code modeling the jitters
            """
#            fit.fitting(fileinput=False,outputfiles=[1,0,0], doGP=doGP,  kernel_id=gp_kernel_id,  minimize_fortran=minimize_fortran,  fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=True,amoeba_starts=ff, print_stat=False, eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value())
            fit.fitting(fileinput=False,outputfiles=[1,1,1], doGP=doGP,  kernel_id=gp_kernel_id,  minimize_fortran=minimize_fortran,  fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=True,amoeba_starts=ff, print_stat=False, eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value(), npoints=self.points_to_draw_model.value(), model_max= self.model_max_range.value(), model_min= self.model_min_range.value())

        elif m_ln == True and doGP == True:       
            fit.fitting(fileinput=False,outputfiles=[1,1,1], doGP=doGP,  kernel_id=gp_kernel_id,  minimize_fortran=minimize_fortran,  fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=True,amoeba_starts=ff,  print_stat=False, eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value(), npoints=self.points_to_draw_model.value(), model_max= self.model_max_range.value(), model_min= self.model_min_range.value())
        
        elif m_ln == False and   minimize_fortran==False:      
            fit.fitting(fileinput=False,outputfiles=[1,1,1], doGP=doGP,  kernel_id=gp_kernel_id,  minimize_fortran=minimize_fortran, fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=True,amoeba_starts=0, print_stat=False,eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value(), npoints=self.points_to_draw_model.value(), model_max= self.model_max_range.value(), model_min= self.model_min_range.value())
        
        else:      
            fit.fitting(fileinput=False,outputfiles=[1,1,1], doGP=doGP,  kernel_id=gp_kernel_id,  minimize_fortran=minimize_fortran, fortran_kill=f_kill, timeout_sec=self.master_timeout.value(),minimize_loglik=m_ln,amoeba_starts=ff, print_stat=False,eps=self.dyn_model_accuracy.value(), dt=self.time_step_model.value(), npoints=self.points_to_draw_model.value(), model_max= self.model_max_range.value(), model_min= self.model_min_range.value())

        for i in range(fit.npl):
             rv.phase_RV_planet_signal(fit,i+1)  

        if auto_fit:
                          
                 
            self.update_labels()
            self.update_gui_params()
            self.update_errors() 
            self.update_a_mass()                    
            self.update_plots()                   
            self.statusBar().showMessage('')           
            self.jupiter_push_vars()




       
    def print_info_for_object(self,text):
        #self.dialog.statusBar().showMessage('Ready')
        self.dialog.setGeometry(300, 300, 450, 250)
        self.dialog.setWindowTitle('Detailed Info')  
 
        self.dialog.text.setPlainText(text)
        self.dialog.text.setReadOnly(True)       
        #self.dialog.setWindowIcon (QtGui.QIcon('logo.png'))        
        self.dialog.show()


    def print_info_credits(self, image=False):
        #self.dialog.statusBar().showMessage('Ready')
        self.dialog_credits.setFixedSize(900, 900)
        self.dialog_credits.setWindowTitle('Credits')  
        #self.dialog.setGeometry(300, 300, 800, 800)
        #self.dialog_credits.acceptRichText(True)
        
        text = ''
        self.dialog_credits.text.setText(text) 
        
        text = "You are using 'The Exo-Striker' (ver. 0.01) \n developed by 3fon3fonov"
        
        self.dialog_credits.text.append(text)

        text = "\n"*15 +"CREDITS:"+"\n"*2 + "This tool uses the publically \n available packages: \n" 
        self.dialog_credits.text.append(text)
        
        text = "* " + "<a href='https://github.com/pyqtgraph/pyqtgraph'>pyqtgraph</a>"
        self.dialog_credits.text.append(text)

        text = "* " + "<a href='https://github.com/dfm/emcee'>emcee</a>" 
        self.dialog_credits.text.append(text) 
        
        text = "* " + "<a href='https://github.com/dfm/celerite'>celerite</a>" 
        self.dialog_credits.text.append(text)  
                                
        text = "* " + "<a href='https://github.com/lkreidberg/batman'>batman-package</a>" 
        self.dialog_credits.text.append(text)
        
        text = "* " + "<a href='https://github.com/hippke/tls'>Transit Least Squares</a>" 
        self.dialog_credits.text.append(text)             

        text = "* " + "<a href='https://www.boulder.swri.edu/~hal/swift.html'>swift</a>" 
        self.dialog_credits.text.append(text)        
                        
        text = "* " + "<a href='https://github.com/jupyter/qtconsole'>qtconsole</a>"
        self.dialog_credits.text.append(text)        

        text = "* " + "<a href='https://github.com/mfitzp/15-minute-apps/tree/master/wordprocessor'>megasolid idiom</a>" 
        self.dialog_credits.text.append(text)  
        
        
        text = "(A few more to be added) \n" 
        self.dialog_credits.text.append(text)   


        #self.dialog_credits.text.setText(text)
        #self.dialog_credits.text.insertHtml(text)
        
        
        text = "\n"*5 + """Note:
Please keep in mind that this software is developed 
mostly for my needs and for fun. I hope, however, 
that you may find it capable to solve your scientific 
problems, too. 

Feedback and help in further developing will be 
highly appreciated!
"""
        self.dialog_credits.text.append(text)   
  
        self.dialog_credits.text.setReadOnly(True)       
        
        self.dialog_credits.setStyleSheet(" QTextEdit{border-image: url(./lib/33_striker.png) 0 0 0 0 stretch stretch;} ")

        #self.dialog.setWindowIcon (QtGui.QIcon('logo.png'))        
        
        self.dialog_credits.show()
        
  

    def run_nest_samp(self):
        global fit
        choice = QtGui.QMessageBox.information(self, 'Warning!', "Not available yet. Okay?", QtGui.QMessageBox.Ok) 


    def find_planets(self):
        global fit 

        # check if RV data is present
        if fit.filelist.ndset <= 0:
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "Not possible to look for planets if there are no RV data loaded. Please add your RV data first. Okay?", QtGui.QMessageBox.Ok)      
             self.button_auto_fit.setEnabled(True)         
             return        

        # the first one on the data GLS
        if fit.gls.power.max() <= fit.gls.powerLevel(self.auto_fit_FAP_level.value()):
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "No significant power on the GLS. Therefore no planets to fit OK?", QtGui.QMessageBox.Ok)      
             self.button_auto_fit.setEnabled(True)                                                           
             return
        
        else:
            if fit.npl !=0:
                for j in range(fit.npl):
                    fit.remove_planet(fit.npl-(j+1))

            mean_anomaly_from_gls = np.degrees((((fit.epoch - float(fit.gls.hpstat["T0"]) )% (fit.gls.hpstat["P"]) )/ (fit.gls.hpstat["P"]) ) * 2*np.pi)
             
            fit.add_planet(fit.gls.hpstat["amp"],fit.gls.hpstat["P"],0.0,0.0,mean_anomaly_from_gls -90.0,90.0,0.0)
            fit.use.update_use_planet_params_one_planet(0,True,True,True,True,True,False,False)     
            self.update_use_from_input_file()   
            self.update_use()                     
            self.optimize_fit(20,m_ln=self.amoeba_radio_button.isChecked(),auto_fit = True)
            
            #now inspect the residuals
            
            for i in range(1,int(self.auto_fit_N_planets.value())):
                
                if fit.gls_o_c.power.max() <= fit.gls_o_c.powerLevel(self.auto_fit_FAP_level.value()):
                    for j in range(fit.npl):
                        fit.use.update_use_planet_params_one_planet(j,True,True,True,True,True,False,False)     
            
                    self.update_use_from_input_file()   
                    self.update_use()                     
                    self.optimize_fit(20,m_ln=self.amoeba_radio_button.isChecked(),auto_fit = True) 
                    self.button_auto_fit.setEnabled(True)     
                    return
                #elif (1/RV_per_res.hpstat["fbest"]) > 1.5:
                else:    
                    mean_anomaly_from_gls = np.degrees((((fit.epoch - float(fit.gls_o_c.hpstat["T0"]) )% (fit.gls_o_c.hpstat["P"]) )/ (fit.gls_o_c.hpstat["P"]) ) * 2*np.pi)
             
                    fit.add_planet(fit.gls_o_c.hpstat["amp"],fit.gls_o_c.hpstat["P"],0.0,0.0,mean_anomaly_from_gls -90.0,90.0,0.0)
                    fit.use.update_use_planet_params_one_planet(i,True,True,True,True,True,False,False)  
                    
                    #print(fit.params.planet_params[2 + 7*(i-1)])
                    #fit.use.update_use_planet_params_one_planet(i,True,True,True,True,True,False,False)  
                   
                    self.update_use_from_input_file()   
                    self.update_use()                     
                    self.optimize_fit(20,m_ln=self.amoeba_radio_button.isChecked(),auto_fit = True)  
                    
                #else:
                 #   continue
                                       
            for j in range(fit.npl):
                fit.use.update_use_planet_params_one_planet(j,True,True,True,True,True,False,False)     
    
            self.update_use_from_input_file()   
            self.update_use()                     
            self.optimize_fit(20,m_ln=self.amoeba_radio_button.isChecked(),auto_fit = True)           
 
        self.button_auto_fit.setEnabled(True)   
 

    def run_auto_fit(self):
        global fit 
        
        self.radioButton_Keplerian.setChecked(True) # this is to be fixed! Only with keplerian fitting th autofit works fine so far.
        self.button_auto_fit.setEnabled(False)         
        
        if fit.npl != 0:        
            choice = QtGui.QMessageBox.information(self, 'Warning!',
                                            "Planets already exist. Do you want to overwrite the analysis?",
                                            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)  
         
            if choice == QtGui.QMessageBox.No:
                self.button_auto_fit.setEnabled(True)         
                return
            elif choice == QtGui.QMessageBox.Yes:
                self.find_planets()
        else:
            self.find_planets()
                

    def minimize_1param(self):
        global fit
        """
        This function must be completely refurbished!!! How to check 
        which QDoubleSpinBox is trigerred? Does everytime one needs to call 
        self.init_fit() ? ? ?
        
        """
        
        self.K1.minimize_signal.connect(lambda: fit.minimize_one_param_K(0)) #TBD!
        self.K1.minimize_signal.connect(self.init_fit) #TBD!       
        self.P1.minimize_signal.connect(lambda: fit.minimize_one_param_P(0)) #TBD!
        self.P1.minimize_signal.connect(self.init_fit) #TBD!     
        self.e1.minimize_signal.connect(lambda: fit.minimize_one_param_e(0)) #TBD!
        self.e1.minimize_signal.connect(self.init_fit) #TBD!  
        self.om1.minimize_signal.connect(lambda: fit.minimize_one_param_w(0)) #TBD!
        self.om1.minimize_signal.connect(self.init_fit) #TBD!  
        self.ma1.minimize_signal.connect(lambda: fit.minimize_one_param_M0(0)) #TBD!
        self.ma1.minimize_signal.connect(self.init_fit) #TBD!  
        
        self.K2.minimize_signal.connect(lambda: fit.minimize_one_param_K(1)) #TBD!
        self.K2.minimize_signal.connect(self.init_fit) #TBD!       
        self.P2.minimize_signal.connect(lambda: fit.minimize_one_param_P(1)) #TBD!
        self.P2.minimize_signal.connect(self.init_fit) #TBD!     
        self.e2.minimize_signal.connect(lambda: fit.minimize_one_param_e(1)) #TBD!
        self.e2.minimize_signal.connect(self.init_fit) #TBD!  
        self.om2.minimize_signal.connect(lambda: fit.minimize_one_param_w(1)) #TBD!
        self.om2.minimize_signal.connect(self.init_fit) #TBD!  
        self.ma2.minimize_signal.connect(lambda: fit.minimize_one_param_M0(1)) #TBD!
        self.ma2.minimize_signal.connect(self.init_fit) #TBD!         
        
        self.K3.minimize_signal.connect(lambda: fit.minimize_one_param_K(2)) #TBD!
        self.K3.minimize_signal.connect(self.init_fit) #TBD!       
        self.P3.minimize_signal.connect(lambda: fit.minimize_one_param_P(2)) #TBD!
        self.P3.minimize_signal.connect(self.init_fit) #TBD!     
        self.e3.minimize_signal.connect(lambda: fit.minimize_one_param_e(2)) #TBD!
        self.e3.minimize_signal.connect(self.init_fit) #TBD!  
        self.om3.minimize_signal.connect(lambda: fit.minimize_one_param_w(2)) #TBD!
        self.om3.minimize_signal.connect(self.init_fit) #TBD!  
        self.ma3.minimize_signal.connect(lambda: fit.minimize_one_param_M0(2)) #TBD!
        self.ma3.minimize_signal.connect(self.init_fit) #TBD!               
        
    def jupiter_push_vars(self):
        global fit        
        self.console_widget.push_vars({'fit':fit})    
        #self.console_widget.push_vars({'pg':pg})    

        #self.console_widget.clear()         
        #self.console_widget.print_text(str("Welcome!"+"\n")) 

       ########################## work in progress ##################################
 
    def getNewses(self):
        global fit, ses_list  
        
        text, okPressed = QtGui.QInputDialog.getText(self, "New session","Name session: (No space and special characters!)", QtGui.QLineEdit.Normal, "")
        if okPressed and text != '':
            
            if len(ses_list) == 0:
                ses_list.append(fit)
                      
            #file_pi = open('.sessions/empty.ses', 'rb')
            #fit_new = dill.load(file_pi)
            #file_pi.close()
            fit_new=rv.signal_fit(name='init')

            fit_new.name=text
            ses_list.append(fit_new)
 
            self.session_list()
            
    def rem_ses(self):
        global fit, ses_list  
        
        ind = self.comboBox_select_ses.currentIndex()
        
        choice = QtGui.QMessageBox.information(self, 'Warning!',
        "Do you really want to remove Session %s"%(ind+1),
                                            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)  
         
        if choice == QtGui.QMessageBox.No:
            return
        elif choice == QtGui.QMessageBox.Yes: # and ind <=0:
            if len(ses_list)==1:
                ses_list.pop(0)         
                self.new_session()
                self.session_list() 
                self.select_session(0)
            else:
            #ses_list[0] = fit
        #elif choice == QtGui.QMessageBox.Yes and ind > 0:
                ses_list.pop(ind)
                self.session_list() 
                self.select_session(ind-1)
            
    def cop_ses(self):
        global fit, ses_list  
        
        ind = self.comboBox_select_ses.currentIndex()
        
        if len(ses_list) == 0:
            ses_list.append(fit)
        if ind <=0:
            fit_new =dill.copy(ses_list[0])
        elif ind > 0:
            fit_new =dill.copy(ses_list[ind])
 
        
        ses_list.append(fit_new)
        self.session_list() 
        self.select_session(ind-1)            
  

    def session_list(self):
        global fit, ses_list
        
        
        if len(ses_list) == 0:
            self.comboBox_select_ses.clear()
            self.comboBox_select_ses.addItem("session 1") 

        elif len(ses_list) != 0:
            self.comboBox_select_ses.clear()
            for i in range(len(ses_list)):
                self.comboBox_select_ses.addItem('session %s'%(i+1),i)                
        #self.select_session(0)

    def select_session(self, index):
        global fit, ses_list

        ind = self.comboBox_select_ses.itemData(index) 
        #print(ind,index,len(ses_list))
        if ind == None:
            return
            #fit = ses_list[0]
        else:
            fit = ses_list[ind]
        #ses_list[ind-1] = fit

        self.check_settings()

        self.init_fit()

        self.update_use_from_input_file()   
        self.update_use()
        self.update_gui_params()
        self.update_params()
        self.update_RV_file_buttons() 
        self.update_color_picker()
        
        if not ind == None:    
            ses_list[ind] = fit

#######################################################################            

    def new_session(self):
        global fit, ses_list
        
        #file_pi = open('.sessions/empty.ses', 'rb')
        #fit_new = dill.load(file_pi)
        #file_pi.close()     
        fit_new=rv.signal_fit(name='init')

        ses_list.append(fit_new)
        self.session_list()
            
    def open_session(self):
        global fit,ses_list
        
        input_file = QtGui.QFileDialog.getOpenFileName(self, 'Open session', '', 'Data (*.ses)')

        if str(input_file[0]) != '':

            file_pi = open(input_file[0], 'rb')
            fit_new = dill.load(file_pi)
            file_pi.close()     
            ses_list.append(fit_new)
            
            #self.check_settings()
            self.session_list()
        

    def save_session(self):
        global fit
        
        output_file = QtGui.QFileDialog.getSaveFileName(self, 'Save session', '', 'Data (*.ses)')
        
        if str(output_file[0]) != '':
            file_pi = open(output_file[0], 'wb')
            dill.dump(fit, file_pi)
            file_pi.close()


    def open_sessions(self):
        global fit, ses_list
        
        input_file = QtGui.QFileDialog.getOpenFileName(self, 'Open session', '', 'Data (*.mses)')

        if str(input_file[0]) != '':

            file_pi = open(input_file[0], 'rb')
            fit2 = dill.load(file_pi)
            file_pi.close()   
        
            choice = QtGui.QMessageBox.information(self, 'Warning!',
                                            "Do you want to overwrite the current sessions? If you choose 'No' will add the session, 'Cancel' will exit",
                                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)  
         
            if choice == QtGui.QMessageBox.No:
                ses_list = ses_list + fit2
            elif choice == QtGui.QMessageBox.Yes:
                ses_list = fit2
            elif choice == QtGui.QMessageBox.Cancel:        
                return         
           #if len(ses_list) == 0: 
          #      ses_list = fit2
          #  else:  
          #      ses_list = ses_list + fit2
    
            self.check_settings()
    
            self.session_list()
            self.select_session(0)

    def save_sessions(self):
        global fit, ses_list

        
        output_file = QtGui.QFileDialog.getSaveFileName(self, 'Save multi-session', '', 'Data (*.mses)')

        if str(output_file[0]) != '':
            file_pi = open(output_file[0], 'wb')
            dill.dump(ses_list, file_pi)
            file_pi.close()


    def quit(self):
        #os.system("rm temp*.vels")
        choice = QtGui.QMessageBox.information(self, 'Warning!',
                                            "Do you want to save the session before you Quit?",
                                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)  
         
        if choice == QtGui.QMessageBox.No:
            self.close()
        elif choice == QtGui.QMessageBox.Yes:
            self.save_session()
        elif choice == QtGui.QMessageBox.Cancel:
            return 
 

################################## MCMC #######################################

    def worker_mcmc_complete(self):
        global fit  
        #fit.print_info(short_errors=False)
        
        self.update_labels()
        self.update_gui_params()
        self.update_errors() 
        self.update_a_mass() 
        
        self.statusBar().showMessage('') 
        #self.console_widget.print_text(str(fit.print_info(short_errors=False))) 
        
        if self.adopt_mcmc_means_as_par.isChecked() or self.adopt_best_lnL_as_pars.isChecked():
            self.init_fit()
 
       # if sys.version_info[0] == 3:
       #     self.print_py3_warning()

    def worker_mcmc(self):
        global fit  
        
        
        if self.radioButton_RV.isChecked():
            fit.rtg = [True,self.do_RV_GP.isChecked(), False]
        elif self.radioButton_transit.isChecked():
            fit.rtg = [False, self.do_RV_GP.isChecked(), True]
        elif self.radioButton_transit_RV.isChecked():
            fit.rtg = [True,self.do_RV_GP.isChecked(), True]
        
        self.button_MCMC.setEnabled(False)
        self.statusBar().showMessage('MCMC in progress....')        
        # check if RV data is present
        if fit.rtg[0] == True and fit.filelist.ndset <= 0:
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "Not possible to run MCMC if there are no RV data loaded. Please add your RV data first. Okay?", QtGui.QMessageBox.Ok)      
             self.button_MCMC.setEnabled(True)  
             self.statusBar().showMessage('') 

             return   
        
        ntran_data = 0
        for i in range(0,10,1):         
            ntran_data += len(fit.tra_data_sets[i]) 
            
        if fit.rtg[2] == True and ntran_data == 0:
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "Not possible to run MCMC if there are no transit data loaded. Please add your transit data first. Okay?", QtGui.QMessageBox.Ok)      
             self.button_MCMC.setEnabled(True)  
             self.statusBar().showMessage('') 

             return             
            
            

        choice = QtGui.QMessageBox.information(self, 'Warning!',
                                            "This will run in the background and may take some time. Results are printed in the 'Stdout/Stderr' tab. Okay?",
                                            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)       
 
         
        if choice == QtGui.QMessageBox.Cancel:
            self.statusBar().showMessage('') 
            self.button_MCMC.setEnabled(True)
            return        
        
        self.check_bounds()
        self.check_priors() 
        fit.model_npoints = self.points_to_draw_model.value()
        
        self.tabWidget_helper.setCurrentWidget(self.tab_info)
        
        
        if self.use_percentile_level.isChecked():
            fit.percentile_level = self.percentile_level.value()
        else:
            fit.percentile_level = 68.3
           
        
        # Pass the function to execute
        worker = Worker(lambda: self.run_mcmc()) # Any other args, kwargs are passed to the run  
        # Execute
        worker.signals.finished.connect(self.worker_mcmc_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
        
    def run_mcmc(self):
        global fit
        
 
        self.check_mcmc_params()
      
        fit = rv.run_mcmc(fit, burning_ph=self.burning_phase.value(), mcmc_ph=self.mcmc_phase.value(), threads=int(self.N_threads.value()), output=False,
        fileoutput=self.save_samples.isChecked(),save_means=self.adopt_mcmc_means_as_par.isChecked(), save_minlnL=self.adopt_best_lnL_as_pars.isChecked())
        
    
        self.button_MCMC.setEnabled(True)            
 
    def change_mcmc_samples_file_name(self):
        global fit
        
        output_file = QtGui.QFileDialog.getSaveFileName(self, 'path and name of the mcmc samples', '', '')
        
        if output_file[0] != '':
            fit.mcmc_sample_file = output_file[0] 
            self.mcmc_samples_change_name.setText(output_file[0])
        else:
            return

    def check_mcmc_params(self):
        global fit
        fit.gaussian_ball = self.init_gauss_ball.value() 
        fit.nwalkers_fact = int(self.nwalkers_fact.value()) 


    def force_mcmc_check_box(self):
        if self.make_corner_plot.isChecked():
            self.save_samples.setChecked(True)
 
                       
################################## Cornerplot #######################################

    def worker_cornerplot_complete(self):
        global fit  
        self.statusBar().showMessage('') 
        self.button_make_cornerplot.setEnabled(True)


    def worker_cornerplot(self):
        global fit  
        
        self.button_make_cornerplot.setEnabled(False)
        self.statusBar().showMessage('Cornerplot in progress....')        
        # check if RV data is present
        if not os.path.exists(fit.mcmc_sample_file):
             choice = QtGui.QMessageBox.information(self, 'Warning!',
             "MCMC file not found. Generate one and try again?", QtGui.QMessageBox.Ok)      
             self.button_make_cornerplot.setEnabled(True)

             return  
 
 
        # Pass the function to execute
        worker_cor = Worker(lambda: self.make_cornerplot()) # Any other args, kwargs are passed to the run  
        # Execute
        worker_cor.signals.finished.connect(self.worker_cornerplot_complete)
        
        # worker.signals.result.connect(self.print_output)
        #worker.signals.finished.connect(self.thread_complete)
       # worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker_cor)
 
            
    def make_cornerplot(self):
        global fit
        rv.cornerplot(fit, fileinput=True)
            
            
      
    def change_corner_plot_file_name(self):
        global fit
        
        output_file = QtGui.QFileDialog.getSaveFileName(self, 'path and name of the corener plot', '', 'Data (*.png)')
        if output_file[0] != '':
            fit.corner_plot_file = output_file[0] 
            self.corner_plot_change_name.setText(output_file[0])   
            
            
       
################################# data inspector ###################################  
        
        
        
    def load_data_inspect(self): 
        global fit
         
        #path = self.tree_view_tab.listview.model().filePath(index)
        path = self.inspector_file
        if path == '':
            return 
        
        filename, file_extension = os.path.splitext(path)  
            
        if file_extension == '.vels':
            fit.add_dataset(self.file_from_path(path), str(path),0.0,1.0)
            self.init_fit()            
            self.update_use_from_input_file()            
            self.update_use()
            self.update_params()
            self.update_RV_file_buttons()        
 
        elif file_extension == '.act':
            
            for i in range(10):
                if len(fit.act_data_sets[i]) == 0:    
                    but_ind = i +1
            
                    fit.add_act_dataset('test', str(path),act_idset =but_ind-1)
         
        
                    self.update_act_file_buttons()
                    self.update_activity_gls_plots(but_ind-1)
                    self.buttonGroup_activity_data.button(but_ind).setText(self.file_from_path(path))
                    return
            
        elif  file_extension == '.tran':
            for i in range(10):
                if len(fit.tra_data_sets[i]) == 0:                 
                    but_ind = i +1
 
                    fit.add_transit_dataset('test', str(path),tra_idset =but_ind-1)
                    self.update_use_from_input_file()            
                    self.update_use()
                    self.update_gui_params()           
                    self.update_params()
                    self.update_tra_file_buttons()
                    self.buttonGroup_transit_data.button(but_ind).setText(self.file_from_path(path))
                    return
           
        else: 
            return
            
    def plot_data_inspect(self, index):
        global fit, colors,pdi 
        # self.sender() == self.treeView
        # self.sender().model() == self.fileSystemModel
        path = self.sender().model().filePath(index)
 
   
        pdi.plot(clear=True,)  
        
        try:    
            x     = np.genfromtxt("%s"%(path),skip_header=0, unpack=True,skip_footer=0, usecols = [0])
            y     = np.genfromtxt("%s"%(path),skip_header=0, unpack=True,skip_footer=0, usecols = [1])
            y_err = np.genfromtxt("%s"%(path),skip_header=0, unpack=True,skip_footer=0, usecols = [2]) 
        except:
            #pdi.addLine(x=[0,1], y=0, pen=pg.mkPen('#ff9933', width=0.8)) 
            pdi.setLabel('bottom', 'x', units='',  **{'font-size':'11pt'})
            pdi.setLabel('left',   'y', units='',  **{'font-size':'11pt'})
            return
 
        pdi.addLine(x=None, y=np.mean(y), pen=pg.mkPen('#ff9933', width=0.8))   
 
        if self.rv_data_size.value() > 2:
            symbolsize = self.rv_data_size.value() -2
        else:
            symbolsize = self.rv_data_size.value() 

    
        pdi.plot(x,y,             
        pen=None, #{'color': colors[i], 'width': 1.1},
        symbol='o',
        symbolPen={'color': fit.colors[0], 'width': 1.1},
        symbolSize=symbolsize,enableAutoRange=True,viewRect=True,
        symbolBrush=fit.colors[0]
        )  
               
        err_ = pg.ErrorBarItem(x=x, y=y,
        symbol='o', height=y_err, beam=0.0, pen=fit.colors[0])   
     
        pdi.addItem(err_)
        
        pdi.autoRange()
 
        
        filename, file_extension = os.path.splitext(path)  
            
        if file_extension == '.vels':
            pdi.setLabel('bottom', 'BJD', units='d',  **{'font-size':'11pt'})
            pdi.setLabel('left',   'RV', units='m/s',  **{'font-size':'11pt'})         
 
        elif file_extension == '.act':
            pdi.setLabel('bottom', 'BJD', units='d',  **{'font-size':'11pt'})
            pdi.setLabel('left',   'y', units='',  **{'font-size':'11pt'})    
            
        elif file_extension == '.tran':      
            pdi.setLabel('bottom', 'BJD', units='d',  **{'font-size':'11pt'})
            pdi.setLabel('left',   'flux', units='',  **{'font-size':'11pt'})

        else:      
            pdi.setLabel('bottom', 'x', units='',  **{'font-size':'11pt'})
            pdi.setLabel('left',   'y', units='',  **{'font-size':'11pt'})
        
 
        self.inspector_file = path     
        self.data_insp_print_info.clicked.connect(lambda: self.print_info_for_object(self.stat_info(x,y,y_err,path)))   

        #self.data_insp_load_data.clicked.connect(lambda: self.load_data_inspect(path))
        
        
    def stat_info(self,x,y,y_err,path):
 
 
        ################## text generator #################
        text_info = """ 
"""
        text_info = text_info +"""%s
-----------------------------------  
"""%path    
        text_info = text_info +"""
N data          :  %s        
        
first epoch     :  %.3f
last epoch      :  %.3f
time span       :  %.3f

min. value      :  %.4f
max. value      :  %.4f
end-to-end      :  %.4f
mean            :  %.4f
median          :  %.4f
r.m.s.          :  %.4f

min error       :  %.4f
max error       :  %.4f
mean error      :  %.4f
median error    :  %.4f

"""%(len(x), x[0], x[-1], x[-1]-x[0], np.min(y), np.max(y), np.max(y)-np.min(y), np.mean(y),  np.median(y), np.sqrt(np.mean(np.square(y))),
np.min(y_err), np.max(y_err),   np.mean(y_err),  np.median(y_err))       
      
     
        return text_info  
              
        
             
            
       
############################# Dispatcher #####################################  

    def fit_dispatcher(self, init=False):
        global fit
   
        if self.radioButton_RV.isChecked():
            fit.rtg = [True,self.do_RV_GP.isChecked(),False]            
            if(init):
                self.worker_RV_fitting(ff=0,m_ln=True, init = init )  
                #print('test')
            else:
                self.worker_RV_fitting(m_ln=self.amoeba_radio_button.isChecked())  
                               
        elif self.radioButton_transit.isChecked(): 
            fit.rtg = [False,False,True]
            if(init):             
                self.worker_transit_fitting(ff=0)  
            else:
                self.worker_transit_fitting()
                                               
        elif self.radioButton_transit_RV.isChecked():
            
            fit.rtg=[True,self.do_RV_GP.isChecked(),True]
            if(init):
                self.worker_transit_fitting(ff=0 )  
            else:
                self.worker_transit_fitting()

 
    
    
    
    
##################  Mute box controlls #############################





    def mute_boxes(self):
        
        ######### TESTS!!!!!!!!!!!###########
        
        if self.radioButton_transit_RV.isChecked() or self.radioButton_transit.isChecked():
            
            
            
            self.ma1.setEnabled(False)
            self.use_ma1.setEnabled(False)
            self.ma2.setEnabled(False)
            self.use_ma2.setEnabled(False)           
            self.ma3.setEnabled(False)
            self.use_ma3.setEnabled(False)  
            self.ma4.setEnabled(False)
            self.use_ma4.setEnabled(False)
            self.ma5.setEnabled(False)
            self.use_ma5.setEnabled(False)           
            self.ma6.setEnabled(False)
            self.use_ma6.setEnabled(False)  
            self.ma7.setEnabled(False)
            self.use_ma7.setEnabled(False)
            self.ma8.setEnabled(False)
            self.use_ma8.setEnabled(False)           
            self.ma9.setEnabled(False)
            self.use_ma9.setEnabled(False)  

            
            self.t0_1.setEnabled(True)
            self.use_t0_1.setEnabled(True)
            self.t0_2.setEnabled(True)
            self.use_t0_2.setEnabled(True)           
            self.t0_3.setEnabled(True)
            self.use_t0_3.setEnabled(True)  
            self.t0_4.setEnabled(True)
            self.use_t0_4.setEnabled(True)
            self.t0_5.setEnabled(True)
            self.use_t0_5.setEnabled(True)           
            self.t0_6.setEnabled(True)
            self.use_t0_6.setEnabled(True)              
            self.t0_7.setEnabled(True)
            self.use_t0_7.setEnabled(True)
            self.t0_8.setEnabled(True)
            self.use_t0_8.setEnabled(True)           
            self.t0_9.setEnabled(True)
            self.use_t0_9.setEnabled(True)              
            

            self.K1.setEnabled(False)
            self.use_K1.setEnabled(False)
            self.K2.setEnabled(False)
            self.use_K2.setEnabled(False)           
            self.K3.setEnabled(False)
            self.use_K3.setEnabled(False)        
            self.K4.setEnabled(False)
            self.use_K4.setEnabled(False)
            self.K5.setEnabled(False)
            self.use_K5.setEnabled(False)           
            self.K6.setEnabled(False)
            self.use_K6.setEnabled(False)                    
            self.K7.setEnabled(False)
            self.use_K7.setEnabled(False)
            self.K8.setEnabled(False)
            self.use_K8.setEnabled(False)           
            self.K9.setEnabled(False)
            self.use_K9.setEnabled(False)                    
            
            

            self.t0_1.setEnabled(True)
            self.use_t0_1.setEnabled(True)
            self.t0_2.setEnabled(True)
            self.use_t0_2.setEnabled(True)           
            self.t0_3.setEnabled(True)
            self.use_t0_3.setEnabled(True) 
            self.t0_4.setEnabled(True)
            self.use_t0_4.setEnabled(True)
            self.t0_5.setEnabled(True)
            self.use_t0_5.setEnabled(True)           
            self.t0_6.setEnabled(True)
            self.use_t0_6.setEnabled(True)             
            self.t0_7.setEnabled(True)
            self.use_t0_7.setEnabled(True)
            self.t0_8.setEnabled(True)
            self.use_t0_8.setEnabled(True)           
            self.t0_9.setEnabled(True)
            self.use_t0_9.setEnabled(True)             
            

            self.pl_rad_1.setEnabled(True)
            self.use_pl_rad_1.setEnabled(True)
            self.pl_rad_2.setEnabled(True)
            self.use_pl_rad_2.setEnabled(True)           
            self.pl_rad_3.setEnabled(True)
            self.use_pl_rad_3.setEnabled(True) 
            self.pl_rad_4.setEnabled(True)
            self.use_pl_rad_4.setEnabled(True)
            self.pl_rad_5.setEnabled(True)
            self.use_pl_rad_5.setEnabled(True)           
            self.pl_rad_6.setEnabled(True)
            self.use_pl_rad_6.setEnabled(True)             
            self.pl_rad_7.setEnabled(True)
            self.use_pl_rad_7.setEnabled(True)
            self.pl_rad_8.setEnabled(True)
            self.use_pl_rad_8.setEnabled(True)           
            self.pl_rad_9.setEnabled(True)
            self.use_pl_rad_9.setEnabled(True)             
            
      
            self.a_sol_1.setEnabled(True)
            self.use_a_sol_1.setEnabled(True)
            self.a_sol_2.setEnabled(True)
            self.use_a_sol_2.setEnabled(True)           
            self.a_sol_3.setEnabled(True)
            self.use_a_sol_3.setEnabled(True)                        
            self.a_sol_4.setEnabled(True)
            self.use_a_sol_4.setEnabled(True)
            self.a_sol_5.setEnabled(True)
            self.use_a_sol_5.setEnabled(True)           
            self.a_sol_6.setEnabled(True)
            self.use_a_sol_6.setEnabled(True)                 
            self.a_sol_7.setEnabled(True)
            self.use_a_sol_7.setEnabled(True)
            self.a_sol_8.setEnabled(True)
            self.use_a_sol_8.setEnabled(True)           
            self.a_sol_9.setEnabled(True)
            self.use_a_sol_9.setEnabled(True)                
            
            
            
            
            if self.radioButton_transit.isChecked():

              
                self.K1.setEnabled(False)
                self.use_K1.setEnabled(False)
                self.K2.setEnabled(False)
                self.use_K2.setEnabled(False)           
                self.K3.setEnabled(False)
                self.use_K3.setEnabled(False)  
                self.K4.setEnabled(False)
                self.use_K4.setEnabled(False)
                self.K5.setEnabled(False)
                self.use_K5.setEnabled(False)           
                self.K6.setEnabled(False)
                self.use_K6.setEnabled(False)                  
                self.K7.setEnabled(False)
                self.use_K7.setEnabled(False)
                self.K8.setEnabled(False)
                self.use_K8.setEnabled(False)           
                self.K9.setEnabled(False)
                self.use_K9.setEnabled(False)                  
 
            else:
                self.K1.setEnabled(True)
                self.use_K1.setEnabled(True)
                self.K2.setEnabled(True)
                self.use_K2.setEnabled(True)           
                self.K3.setEnabled(True)
                self.use_K3.setEnabled(True)                
                self.K4.setEnabled(True)
                self.use_K4.setEnabled(True)
                self.K5.setEnabled(True)
                self.use_K5.setEnabled(True)           
                self.K6.setEnabled(True)
                self.use_K6.setEnabled(True)                   
                self.K7.setEnabled(True)
                self.use_K7.setEnabled(True)
                self.K8.setEnabled(True)
                self.use_K8.setEnabled(True)           
                self.K9.setEnabled(True)
                self.use_K9.setEnabled(True)    
              
            
        elif self.radioButton_RV.isChecked():

            self.K1.setEnabled(True)
            self.use_K1.setEnabled(True)
            self.K2.setEnabled(True)
            self.use_K2.setEnabled(True)           
            self.K3.setEnabled(True)
            self.use_K3.setEnabled(True)           
            self.K4.setEnabled(True)
            self.use_K4.setEnabled(True)
            self.K5.setEnabled(True)
            self.use_K5.setEnabled(True)           
            self.K6.setEnabled(True)
            self.use_K6.setEnabled(True)                   
            self.K7.setEnabled(True)
            self.use_K7.setEnabled(True)
            self.K8.setEnabled(True)
            self.use_K8.setEnabled(True)           
            self.K9.setEnabled(True)
            self.use_K9.setEnabled(True)                   
 
 
            self.ma1.setEnabled(True)
            self.use_ma1.setEnabled(True)
            self.ma2.setEnabled(True)
            self.use_ma2.setEnabled(True)           
            self.ma3.setEnabled(True)
            self.use_ma3.setEnabled(True)   
            self.ma4.setEnabled(True)
            self.use_ma4.setEnabled(True)
            self.ma5.setEnabled(True)
            self.use_ma5.setEnabled(True)           
            self.ma6.setEnabled(True)
            self.use_ma6.setEnabled(True)               
            self.ma7.setEnabled(True)
            self.use_ma7.setEnabled(True)
            self.ma8.setEnabled(True)
            self.use_ma8.setEnabled(True)           
            self.ma9.setEnabled(True)
            self.use_ma9.setEnabled(True)               
  
 
            self.t0_1.setEnabled(False)
            self.use_t0_1.setEnabled(False)
            self.t0_2.setEnabled(False)
            self.use_t0_2.setEnabled(False)           
            self.t0_3.setEnabled(False)
            self.use_t0_3.setEnabled(False) 
            self.t0_4.setEnabled(False)
            self.use_t0_4.setEnabled(False)
            self.t0_5.setEnabled(False)
            self.use_t0_5.setEnabled(False)           
            self.t0_6.setEnabled(False)
            self.use_t0_6.setEnabled(False)             
            self.t0_7.setEnabled(False)
            self.use_t0_7.setEnabled(False)
            self.t0_8.setEnabled(False)
            self.use_t0_8.setEnabled(False)           
            self.t0_9.setEnabled(False)
            self.use_t0_9.setEnabled(False)             
 
            self.pl_rad_1.setEnabled(False)
            self.use_pl_rad_1.setEnabled(False)
            self.pl_rad_2.setEnabled(False)
            self.use_pl_rad_2.setEnabled(False)           
            self.pl_rad_3.setEnabled(False)
            self.use_pl_rad_3.setEnabled(False) 
            self.pl_rad_4.setEnabled(False)
            self.use_pl_rad_4.setEnabled(False)
            self.pl_rad_5.setEnabled(False)
            self.use_pl_rad_5.setEnabled(False)           
            self.pl_rad_6.setEnabled(False)
            self.use_pl_rad_6.setEnabled(False)             
            self.pl_rad_7.setEnabled(False)
            self.use_pl_rad_7.setEnabled(False)
            self.pl_rad_8.setEnabled(False)
            self.use_pl_rad_8.setEnabled(False)           
            self.pl_rad_9.setEnabled(False)
            self.use_pl_rad_9.setEnabled(False)             
            
            self.a_sol_1.setEnabled(False)
            self.use_a_sol_1.setEnabled(False)
            self.a_sol_2.setEnabled(False)
            self.use_a_sol_2.setEnabled(False)           
            self.a_sol_3.setEnabled(False)
            self.use_a_sol_3.setEnabled(False) 
            self.a_sol_4.setEnabled(False)
            self.use_a_sol_4.setEnabled(False)
            self.a_sol_5.setEnabled(False)
            self.use_a_sol_5.setEnabled(False)           
            self.a_sol_6.setEnabled(False)
            self.use_a_sol_6.setEnabled(False)               
            self.a_sol_7.setEnabled(False)
            self.use_a_sol_7.setEnabled(False)
            self.a_sol_8.setEnabled(False)
            self.use_a_sol_8.setEnabled(False)           
            self.a_sol_9.setEnabled(False)
            self.use_a_sol_9.setEnabled(False)     

            
###########################  GUI events #############################            

    def grab_screen(self):
        p = QtWidgets.QWidget.grab(self)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save image', '', '')
        p.save(filename[0], 'jpg')
        #label.setPixmap(p)        # just for fun :)
        
    def keyPressEvent(self, event):
        global fit
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.update_use()
            self.update_params() 
            #self.init_fit()
            self.fit_dispatcher( init=True)
            return
       # super(Settings, self).keyPressEvent(event)  
       
   # def print_py3_warning(self):
        #self.console_widget.clear()                            
   #     self.console_widget.print_text(str("You are using Python3! The 'stdout/stderr' widget (so far) does not work with Py3. For system output see the shell you started the GUI"+"\n"))
            

############################# Tab selector (not ready) ################################  

    def tab_selected(self,ind):

        if ind == 4:
            self.update_activity_data_plots(self.comboBox_act_data.currentIndex())        
        if ind == 5:
            self.update_correlations_data_plots()
 
    
  
 
#############################  Color control ################################  

    def update_color_picker(self):
        global fit
        
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        #font.setWeight(75)
        
 
        for i in range(10):
            self.buttonGroup_color_picker.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])
            self.buttonGroup_color_picker.button(i+1).setFont(font)              

            self.buttonGroup_symbol_picker.button(i+1).setStyleSheet("color: %s;"%fit.colors[i])  
            self.buttonGroup_symbol_picker.button(i+1).setText(fit.pyqt_symbols_rvs[i]) 
            self.buttonGroup_symbol_picker.button(i+1).setFont(font)              
            
          
    def get_color(self):
        global fit
        
        but_ind = self.buttonGroup_color_picker.checkedId()   
        colorz = QtGui.QColorDialog.getColor()
        
        if colorz.isValid():
            fit.colors[but_ind-1]=colorz.name()   
            self.update_color_picker()
            self.update_act_file_buttons()      
            self.update_RV_file_buttons() 
            self.update_tra_file_buttons() 
            self.update_RV_plots() 
            self.update_extra_plots()            
            self.update_transit_plots() 
            #self.update_activity_data_plots() 
            #self.update_activity_gls_plots()     
        else:
            return



############################# Symbol controls ################################  

            
    def get_symbol(self):
        global fit

    
        but_ind = self.buttonGroup_symbol_picker.checkedId()   
 
        but_n = self.dialog_symbols.get_radio()
        
        
        if but_n != None:
            fit.pyqt_symbols_rvs[but_ind-1] = symbols[but_n-1]
            self.update_color_picker()
            self.update_act_file_buttons()      
            self.update_RV_file_buttons() 
            self.update_tra_file_buttons() 
            self.update_RV_plots() 
            self.update_extra_plots()
            self.update_transit_plots()     
        else:
            return    
 
       # print(self.dialog_symbols.do_test)
       
#############################  TEST ZONE ################################  
      
   # def layout_widgets(layout):
    #   return (layout.itemAt(i) for i in range(layout.count()))

    def rv_plot_phase_chage(self):
        global fit        
        
        #RVphase = self.RV_phase_slider.value()
        #print(RVphase)
        #self.phase_plots(1, offset = RVphase)
        ind = self.comboBox_extra_plot.currentIndex()
        if ind+1 <= fit.npl:
            self.phase_plots(ind+1)
        else:
            return
        
        
    def check_settings(self):
        global fit

        mixed_fit_use = [self.mix_pl_1,self.mix_pl_2,self.mix_pl_3,
                         self.mix_pl_4,self.mix_pl_5,self.mix_pl_6,
                         self.mix_pl_7,self.mix_pl_8,self.mix_pl_9 ]
        
        self.use_mix_fitting.setChecked(bool(fit.mixed_fit[0][0]))
        
        for i in range(9):
            mixed_fit_use[i].setChecked(bool(fit.mixed_fit[1][i]))
        #print("TESTTTT")
            
        self.time_step_model.setValue(fit.time_step_model)
        self.dyn_model_accuracy.setValue(fit.dyn_model_accuracy)
        self.dyn_model_to_kill.setValue(fit.dyn_model_to_kill)
        self.kep_model_to_kill.setValue(fit.kep_model_to_kill)
        self.master_timeout.setValue(fit.master_timeout)    
    
                


    def set_RV_GP(self):
        global fit
        
        if self.use_GP_sho_kernel.isChecked():
            fit.gp_kernel = 'SHOKernel'  
        elif self.use_GP_rot_kernel.isChecked():
            fit.gp_kernel = 'RotKernel'
            
            

      
    def check_RV_symbol_sizes(self):
        global fit
        
       # for i in range(10):
        fit.pyqt_symbols_size_rvs[0] = self.rv_data_size_1.value()
        fit.pyqt_symbols_size_rvs[1] = self.rv_data_size_2.value()
        fit.pyqt_symbols_size_rvs[2] = self.rv_data_size_3.value()
        fit.pyqt_symbols_size_rvs[3] = self.rv_data_size_4.value()
        fit.pyqt_symbols_size_rvs[4] = self.rv_data_size_5.value()
        fit.pyqt_symbols_size_rvs[5] = self.rv_data_size_6.value()
        fit.pyqt_symbols_size_rvs[6] = self.rv_data_size_7.value()
        fit.pyqt_symbols_size_rvs[7] = self.rv_data_size_8.value()
        fit.pyqt_symbols_size_rvs[8] = self.rv_data_size_9.value()
        fit.pyqt_symbols_size_rvs[9] = self.rv_data_size_10.value()
        
 
        #print(self.gridLayout_72)
       # for w in self.layout_widgets(self.gridLayout_72):
      #      print(w)
        
        
    def file_from_path(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
    

     
################################################################################################
    
    
    
    
    def __init__(self):
        global fit

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
       # self.showMaximized()

        self.setupUi(self)
        
        self.initialize_buttons()
        self.initialize_plots()   
                
#        self.init_fit()
        
        ###################### Console #############################

        self.console_widget = ConsoleWidget_embed(font_size = 8)
        # add the console widget to the user interface
        # push some variables to the console
        self.console_widget.push_vars({"rv": rv,
                                "np": np,
                                "fit": fit,
                                #"plt": plt,
                                #"clc": self.clc,
                                #'app': self
                                })        
        
        
        #self.console_widget = ConsoleWidget_embed(font_size = 10)
        
        self.terminal_embeded.addTab(self.console_widget, "Jupyter")
        
        ###################### Console #############################
        
       
       # self.terminal_embeded.addTab(self.tree_view_tab, "tree")
      
        
        if sys.platform[0:5] == "linux":
            self.terminal_embeded.addTab(terminal.mainWindow(), "Bash shell")        
        self.terminal_embeded.addTab(pg_console.ConsoleWidget(), "pqg shell")  
        
        
        #self.gridLayout_116.addWidget(terminal.EmbTerminal())
 
        self.gridLayout_text_editor.addWidget(text_editor_es.MainWindow())       
        self.gridLayout_calculator.addWidget(calc.Calculator())  
        
        #################### data inspector ########################
                        
        self.tree_view_tab = Widget_tree()        
       # self.gridLayout_file_tree.setRowStretch(0, 6)
        self.gridLayout_file_tree.setRowStretch(1, 4)
        self.gridLayout_file_tree.addWidget(self.tree_view_tab)

        
        self.tree_view_tab.listview.clicked.connect(self.plot_data_inspect)
        self.data_insp_load_data.clicked.connect(self.load_data_inspect)  
        
        
        
        #################### stdout pipe ########################
       
        #if sys.version_info[0] == 3:
        self.pipe_text = MyDialog()
        self.gridLayout_stdout.addWidget(self.pipe_text)  
   
        #################### credits  ########################
    
        self.dialog = print_info(self)
        self.dialog_credits = print_info(self)
       
        self.load_fort_in_file.clicked.connect(self.showDialog_fortran_input_file)

        self.buttonGroup_4.buttonClicked.connect(self.showDialog_RV_input_file)
        self.buttonGroup_remove_RV_data.buttonClicked.connect(self.remove_RV_file)
 
        self.buttonGroup_activity_data.buttonClicked.connect(self.showDialog_act_input_file)
        self.buttonGroup_remove_activity_data.buttonClicked.connect(self.remove_act_file)     
        
        self.buttonGroup_transit_data.buttonClicked.connect(self.showDialog_tra_input_file)
        self.buttonGroup_remove_transit_data.buttonClicked.connect(self.remove_tra_file)         
        
        self.buttonGroup_use.buttonClicked.connect(self.update_use)
        self.buttonGroup_mixed_fitting.buttonClicked.connect(self.update_mixed_fitting)
        
        self.button_orb_evol.clicked.connect(self.worker_Nbody) 
        self.button_MCMC.clicked.connect(self.worker_mcmc)
        self.button_nest_samp.clicked.connect(lambda: self.run_nest_samp())
        
        
        self.button_make_cornerplot.clicked.connect(self.worker_cornerplot)
        
        self.corner_plot_change_name.clicked.connect(self.change_corner_plot_file_name)
        self.mcmc_samples_change_name.clicked.connect(self.change_mcmc_samples_file_name)
        
        ########## RV fitting ########################
        
        self.button_init_fit.clicked.connect(lambda: self.fit_dispatcher(init=True))
        self.button_fit.clicked.connect(lambda: self.fit_dispatcher())        
        self.button_auto_fit.clicked.connect(lambda: self.run_auto_fit())
        self.minimize_1param()

        self.radioButton_Dynamical.toggled.connect(self.update_dyn_kep_flag)
        self.radioButton_Keplerian.toggled.connect(self.update_dyn_kep_flag)
        

        ############ Sessions #################
        
        self.actionNew_session.triggered.connect(self.new_session)
        self.actionOpen_session.triggered.connect(self.open_session)
        self.actionSave_session.triggered.connect(self.save_session)
        self.actionSave_multi_sesion.triggered.connect(self.save_sessions)
        self.actionOpen_multi_session.triggered.connect(self.open_sessions) 
        #self.comboBox_extra_plot.activated.connect(self.change_extra_plot)      
        self.comboBox_select_ses.activated.connect(self.select_session)
        self.session_list()
        self.new_ses.clicked.connect(self.getNewses)
        self.copy_ses.clicked.connect(self.cop_ses)
        self.remove_ses.clicked.connect(self.rem_ses)
  
        self.actiongrab_screen.triggered.connect(self.grab_screen) 
        self.actionvisit_TRIFON_on_GitHub.triggered.connect(lambda: webbrowser.open('https://github.com/3fon3fonov/trifon'))    
        self.actionCredits.triggered.connect(lambda: self.print_info_credits())
        

        self.jitter_to_plots.stateChanged.connect(self.update_plots)
        
        self.init_correlations_combo()
        self.init_activity_combo()
        self.init_scipy_combo()
        self.comboBox_scipy_minimizer_1.activated.connect(self.check_scipy_min)
        self.comboBox_scipy_minimizer_2.activated.connect(self.check_scipy_min)
        
        
        self.init_gls_norm_combo()
        self.gls_norm_combo.activated.connect(self.update_plots) 

        
        self.setWindowIcon(QtGui.QIcon('./lib/33_striker.png'))
        
        self.radioButton_act_GLS_period.toggled.connect(lambda: self.update_activity_gls_plots(self.comboBox_act_data_gls.currentIndex()))
       
        self.comboBox_act_data_gls.activated.connect(lambda: self.update_activity_gls_plots(self.comboBox_act_data_gls.currentIndex())) 
        self.comboBox_act_data.activated.connect(lambda: self.update_activity_data_plots(self.comboBox_act_data.currentIndex())) 
       
        self.comboBox_corr_1.activated.connect(self.update_correlations_data_plots) 
        self.comboBox_corr_2.activated.connect(self.update_correlations_data_plots) 
        self.plot_corr_err.stateChanged.connect(self.update_correlations_data_plots)
        self.plot_corr_coef.stateChanged.connect(self.update_correlations_data_plots)        

        self.do_RV_GP.stateChanged.connect(self.rv_GP_set_use)

                
        self.color_corr.clicked.connect(self.get_corr_color)
        self.corr_x_label.clicked.connect(self.corr_plot_x_labels)
        self.corr_y_label.clicked.connect(self.corr_plot_y_labels)

 
    
        self.tab_timeseries_RV.currentChanged.connect(self.tab_selected)


        self.radioButton_RV_o_c_GLS_period.toggled.connect(self.update_RV_o_c_GLS_plots)
        self.radioButton_RV_GLS_period.toggled.connect(self.update_RV_GLS_plots)
        
        self.mute_boxes()
        self.radioButton_transit_RV.toggled.connect(self.mute_boxes)
        self.radioButton_transit.toggled.connect(self.mute_boxes)
        self.radioButton_RV.toggled.connect(self.mute_boxes)


        self.radioButton_RV_WF_period.toggled.connect(self.update_WF_plots)

        self.calc_TLS.clicked.connect(self.worker_tls)


        self.quit_button.clicked.connect(self.quit)
 
        self.jupiter_push_vars()
        
        self.update_color_picker()
        self.buttonGroup_color_picker.buttonClicked.connect(self.get_color)    
        
        
        self.dialog_symbols = show_symbols(self)
        self.buttonGroup_symbol_picker.buttonClicked.connect(self.get_symbol) 
        
        self.buttonGroup_use_RV_GP_kernel.buttonClicked.connect(self.set_RV_GP)   
        

        self.RV_phase_slider.sliderReleased.connect(self.rv_plot_phase_chage)       
        
        self.check_settings()

        self.threadpool = QtCore.QThreadPool()
        #self.threadpool.setMaxThreadCount(cpu_count())    
        
        

        #self.treeWidget = tree_view.Widget() #.setModel(self.tree_view)

        print("Hi there! Here you can get some more information from the tool's workflow, stdout/strerr, and piped results.")



#Function Main START
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TRIFON()
    window.show()
    sys.exit(app.exec_())
#Function Main END


if __name__ == '__main__':
    main() 











