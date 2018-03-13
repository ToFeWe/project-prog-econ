"""
A module which creates Table 1 in the final paper. The calculations for this 
have been performed in the module *calc_simulation_subagging*, which can be 
found under *src.analysis.main_simulation* and has been described
in :ref:`analysis`.

"""

import pickle
import json
import numpy as np

from bld.project_paths import project_paths_join as ppj


def make_table(models):
    """ A function to create the only table in the final paper.
    
    Parameters
    ----------
    models: list of shape = 2
        The list of regression functions that should be contained in the table.
        Must be of length 2. In the specification chosen in the paper, it will 
        plot the Friedman 1 Model and the Linear Model.
        
    """
    # Set different table rows with placeholders.
    table_row_multi = ( r'& {meth} & {mse:.2f} & {var:.2f} &'
                        r'\textcolor{{red}}{{{bias:.2f}}} &'
                        r' \multirow{{2}}{{*}}{{{rel:.2f}}}\tabularnewline'
                        '\n')
    table_row_plain = (r'& {meth} & \textcolor{{red}}{{{mse:.2f}}} &' 
                       r'\textcolor{{red}}{{{var:.2f}}} &'
                       r'{bias:.2f} &\tabularnewline')
    
    with open(ppj("OUT_TABLES", 'table_bagging.tex'), 'w') as tex_file:
        tex_file.write('\\begin{tabular}{ l l c c c c}\n')
        tex_file.write('\\toprule\n')
        tex_file.write('\\textbf{Model} & \\textbf{Method} & \\textbf{MSPE} &'
                       '\\textbf{Variance} & \\textbf{Bias$^{2}$} & '
                       '\\textbf{Relative Error}\\tabularnewline\n')
        tex_file.write('\\toprule\n')

        for index, model in enumerate(models):
            if index is not 0:
                tex_file.write('\\midrule\n')
            if model is 'friedman':
                tex_file.write('\\multirow{2}{*}{Friedman \# 1}\n')
            elif model is 'linear':
                tex_file.write('\\multirow{2}{*}{Linear}\n')

            with open(ppj("OUT_ANALYSIS_MAIN", "output_subagging_{}.pickle"
                          .format(model)), "rb") as in_file:
                output_subagging = pickle.load(in_file)
            
            # Calculate the realtive error for the model.
            rel_error = ((  output_subagging['subagging'][-1,0] -
                            output_subagging['bagging'][0]) / 
                            output_subagging['subagging'][-1,0])

            tex_file.write(table_row_multi.format(meth='Tree',
                                            mse=output_subagging['subagging'][-1,0],
                                            var=output_subagging['subagging'][-1,2],
                                            bias=output_subagging['subagging'][-1,1],
                                            rel= rel_error
            ))
            tex_file.write(table_row_plain.format(meth='Bagging',
                                            mse=output_subagging['bagging'][0],
                                            var=output_subagging['bagging'][2],
                                            bias=output_subagging['bagging'][1]
            ))

        tex_file.write('\\bottomrule\n')
        tex_file.write('\\end{tabular}')


if __name__ == '__main__':
    # For the table of the paper, we only use the 'friedman' and the 'linear' 
    # model as for the main plots.
    dgp_models_in_table = ['friedman', 'linear']

    make_table(dgp_models_in_table)
