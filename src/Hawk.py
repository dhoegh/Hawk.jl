# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:57:57 2013

@author: Daniel Høegh
"""
from __future__ import print_function
from __future__ import division
import matplotlib.pyplot as plt
import subprocess
import os, time
import re

rcdef = plt.rcParams.copy()

def latexplot(page_ratio=1, aspect_ratio=(np.sqrt(5)-1.0)/2.0): # Aesthetic ratio
    """
    A function to create latex plots without scaling them. Input the ratio of the page width it should fill, it takes into acount the there is 8mm in hspace.
    Please use plt.savefig('test.pdf'), because it will save the figure so all the text is inside the figure or use the plt.tight_layout(),
    example of use if you only would like to apply it to one plot::
        with Hawk.latexplot(0.5):
            plt.figure()
            plt.plot(x, y)
            plt.xlabel('distance [m]')
            plt.ylabel('stress [MPa')
            plt.savefig('test.pdf')

    if you would like to apply to all plots::

        Hawk.latexplot(1)

    """
    number_of_plot=1/page_ratio
    # imperical 25mm is added i think it's due to tight layout                    equivilent to 8 mm of hspace
    fig_width_mm = (160+25)/number_of_plot-(8*number_of_plot-1) # Get this from LaTeX using \showthe\columnwidth 426 pt
    inches_per_mm = 1.0/25.4               # Convert pt to inch     
    fig_width = fig_width_mm*inches_per_mm  # width in inches
    fig_height = fig_width*aspect_ratio      # height in inches
    fig_size =  [fig_width,fig_height]

    plt.rcParams['backend'] = 'pdf'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] =10
    plt.rcParams['legend.fontsize'] =10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['text.usetex'] = True
    plt.rcParams['savefig.bbox'] ='tight'
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['figure.figsize'] = fig_size
    plt.rcParams['savefig.pad_inches'] = 0.04 #inch
    plt.rcParams['legend.numpoints'] = 1 #defines so there only one point in the legend
    plt.rcParams['axes.formatter.limits'] =  -4, 4 # use scientific notation if log10
                                                  # of the axis range is smaller than the
                                                  # first or larger than the second

    plt.rcParams['lines.markersize'] = 4
    #maybe get some legend paremeter in here since there is much space in a small legend
    ratio_lengend = 1/4.3311043306095 #page_ratio/fig_height with default aspect_ratio.
    ratio_lengend *= fig_height # this is done to convert old format to be defined by height instead of width
    plt.rcParams['legend.handlelength'] = 1.2+0.6*ratio_lengend     # the length of the legend lines in fraction of fontsize
    plt.rcParams['legend.handletextpad'] = 0.2+0.6*ratio_lengend   # the space between the legend line and legend text in fraction of fontsize
    plt.rcParams['legend.labelspacing'] =  0.1+0.4*ratio_lengend   # the vertical space between the legend entries in fraction of fontsize
    plt.rcParams['legend.borderpad'] = 0.4+0.2*ratio_lengend    # border whitespace in fontsize units
    plt.rcParams['lines.markeredgewidth'] = 0.25*ratio_lengend     # the line width around the marker symbol

    return

def latexplot_reset():
    plt.rcParams.update(rcdef)
    
def runansys(inputfile,ansys15=False):
    """
    Input realative path to the input file from script folder, example::

        Hawk.runansys('plane_stress-strain//plane_strain.inp')

    """
    if os.path.isfile(inputfile)==False:
        print('\nFile does not exist\n')
        return

    old_dir=os.getcwd()
    filename=os.path.basename(inputfile)
    try:
        os.chdir(os.path.dirname(inputfile))
    except WindowsError:
        pass
    Ansys_out='AnsysOutputWindow.txt'

    if ansys15:
        filestr = 'start "ANSYS" /B /min /wait "C:\\Program files\\ANSYS Inc\\v150\\ANSYS\\bin\\winx64\\ansys150" -np 4 -b -p ane3fl -i "'+filename+'" -o '+Ansys_out
    else: 
        filestr = 'start "ANSYS" /B /min /wait "C:\\Program files\\ANSYS Inc\\v145\\ANSYS\\bin\\winx64\\ansys145" -np 4 -b -p ane3fl -i "'+filename+'" -o '+Ansys_out
        #                   ^    ^   ^
        #                   1    2   3
        # 1) is title of window needs to be there if a string is called to be execution
        # 2) says it should not create a new window. 3) It should minimized.
    env = os.environ.copy()
    env['ANSWAIT']='1' 
    env['ANSYS_LOCK']='OFF'
    #Call ansys in batch mode
    o=subprocess.call(filestr, shell=True, env=env)
    #print(o)
    if o in [1,7,100]:
        print('\nAnsys returned non sucesfull se following error log\n')
        with open(Ansys_out,'r') as f:
            content=f.read()
            print('-'*70)
                                                       
            print(''.join(re.findall(r'\*\*\* ERROR \*\*\*.*?(?=\*{3})',content,re.DOTALL)))
            #                                               ^  ^  ^
            #                                               1  2  3
            # "3" makes so it matches ***, "2" make the regex look ahead of 
            # current position, "1" makes the regex math the minimum regex that 
            # fulfill the regex
            print('-'*70)
        os.chdir(old_dir)
        raise RuntimeError('ANSYS did not run')
    os.chdir(old_dir)    
    #A bat file to run the equavilant looks like
    """
    @echo off
    rem This batch file is placed in our working directory: "C:\FEM\Bracket"
    SET ANSWAIT=1
    set ANSYS_LOCK=OFF
    "C:\Program files\ANSYS Inc\v145\ANSYS\bin\winx64\ansys145" -b -p ane3fl -i "Specimen_buckling.inp" -o "AnsysOutputWindow.txt"
    """

    
def ansys_eps():
    """
    This is used together with an ansys plot macro that gennerates a eps-files,
    all eps-files in cwd is converted into one pdf-file using latex
    """
    import glob, os
    files=glob.glob('*.eps')
    
    latexpath=r'"C:\Program Files\MiKTeX 2.9\miktex\bin\x64\pdflatex.exe"'
    out_file=[
r"""
\documentclass[12pt,landscape]{article}
\usepackage{graphicx}
\usepackage{epstopdf}
\usepackage[paperwidth=8.02in, paperheight=6.1in]{geometry}
\usepackage[0.01mm]{fullpage}
\begin{document}
\pagenumbering{gobble}% Remove page numbers (and reset to 1)
"""
]
    for file in files:
        out_file+= [
r"""\clearpage
\begin{figure}
\includegraphics[trim=4cm 4cm 4.4cm 4.4cm, angle=-90,width=1\textwidth]{%s}
\end{figure}"""%file]
    out_file+=[r"\end{document}"]
    open('out.tex','w').write('\n'.join(out_file))
    import tempfile
    name=time.strftime('%y%m%d_%H%M%S')
    os.system('call '+latexpath+' -interaction=nonstopmode -quiet -aux-directory=%s -job-name=%s out.tex'%(tempfile.gettempdir(),name))
    #start /min makes it start without hanging the python script on closing
    os.system('start /min '+name+'.pdf')
    os.remove('out.tex')
    for file in files:
        
        os.remove(file)
        try:
            os.remove(file[:-4]+'-eps-converted-to.pdf')
        except WindowsError:
            pass
